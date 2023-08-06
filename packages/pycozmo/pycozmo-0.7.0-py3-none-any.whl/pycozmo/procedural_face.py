"""

Cozmo procedural face rendering.

"""

from typing import Optional, List

from PIL import Image, ImageDraw


__all__ = [
    "ProceduralLid",
    "ProceduralEye",
    "ProceduralFace",
]


DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 64

DEFAULT_EYE_WIDTH = 28
DEFAULT_EYE_HEIGHT = 40

RESAMPLE = Image.NEAREST


class ProceduralBase(object):

    def __init__(self,
                 width: int,
                 height: int):
        self.width = int(width)
        self.height = int(height)
        self.eye_width = int(width * (DEFAULT_EYE_WIDTH / DEFAULT_WIDTH))
        self.eye_height = int(height * (DEFAULT_EYE_HEIGHT / DEFAULT_HEIGHT))
        self.half_eye_width = self.eye_width // 2
        self.half_eye_height = self.eye_height // 2
        self.scale_factor_lid_height = int(1.2 * self.eye_width)
        self.scale_factor_lid_bend = int(1.2 * self.half_eye_width)


class ProceduralLid(ProceduralBase):

    def __init__(self,
                 offset: int = 0,
                 angle_offset: float = 0.0,
                 y: float = 0.0,
                 angle: float = 0.0,
                 bend: float = 0.0,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super(ProceduralLid, self).__init__(width, height)
        self.offset = int(offset)
        self.angle_offset = float(angle_offset)
        self.y = float(y)
        self.angle = float(angle)
        self.bend = float(bend)
        self.black = Image.new("1", (self.width * 2, self.height * 2), color=0)

    def render(self, im: Image) -> None:
        # Lid image
        lid = Image.new("1", (self.width * 2, self.height * 2), color=0)

        draw = ImageDraw.Draw(lid)

        # Draw lid
        lid_height = int(self.eye_height * self.y)
        x1 = self.width - self.scale_factor_lid_height
        y1 = self.height - 1 - self.half_eye_height
        x2 = self.width + self.scale_factor_lid_height
        y2 = self.height - 1 + lid_height
        draw.rectangle(((x1, y1), (x2, y2)), fill=1)

        bend_height = int(self.eye_height * (1.0 - self.y) * self.bend)
        x3 = self.width - self.scale_factor_lid_bend
        y3 = self.height - 1 + lid_height - bend_height
        x4 = self.width + self.scale_factor_lid_bend
        y4 = self.height - 1 + lid_height + bend_height
        draw.chord(((x3, y3), (x4, y4)), 0, 180, fill=1)

        # Rotate
        lid = lid.rotate(self.angle + self.angle_offset, resample=RESAMPLE, expand=0)

        # Translate and compose
        location = ((im.size[0] - lid.size[0]) // 2,
                    (im.size[1] - lid.size[1]) // 2 + self.offset)
        im.paste(self.black, location, lid)


class ProceduralEye(ProceduralBase):

    def __init__(self,
                 offset: int = 0,
                 center_x: int = 0,
                 center_y: int = 0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 angle: float = 0.0,
                 lower_inner_radius_x: float = 0.5,
                 lower_inner_radius_y: float = 0.5,
                 lower_outer_radius_x: float = 0.5,
                 lower_outer_radius_y: float = 0.5,
                 upper_inner_radius_x: float = 0.5,
                 upper_inner_radius_y: float = 0.5,
                 upper_outer_radius_x: float = 0.5,
                 upper_outer_radius_y: float = 0.5,
                 upper_lid_y: float = 0.0,
                 upper_lid_angle: float = 0.0,
                 upper_lid_bend: float = 0.0,
                 lower_lid_y: float = 0.0,
                 lower_lid_angle: float = 0.0,
                 lower_lid_bend: float = 0.0,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT):
        super(ProceduralEye, self).__init__(width, height)
        self.x_factor = 0.55
        self.y_factor = 0.25
        self.corner_radius = (self.width / 20 + self.height / 10)
        self.offset = int(offset)
        self.center_x = int(center_x)
        self.center_y = int(center_y)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.angle = float(angle)
        self.lower_inner_radius_x = float(lower_inner_radius_x)
        self.lower_inner_radius_y = float(lower_inner_radius_y)
        self.lower_outer_radius_x = float(lower_outer_radius_x)
        self.lower_outer_radius_y = float(lower_outer_radius_y)
        self.upper_inner_radius_x = float(upper_inner_radius_x)
        self.upper_inner_radius_y = float(upper_inner_radius_y)
        self.upper_outer_radius_x = float(upper_outer_radius_x)
        self.upper_outer_radius_y = float(upper_outer_radius_y)
        self.lids = (
            ProceduralLid(-self.half_eye_height, 0.0, upper_lid_y, upper_lid_angle, upper_lid_bend,
                          self.width, self.height),
            ProceduralLid(self.half_eye_height + 1, 180.0, lower_lid_y, lower_lid_angle, lower_lid_bend,
                          self.width, self.height)
        )

    def _render_inner_rect(self, draw: ImageDraw, y1: int, x2: int, y2: int) -> None:
        x3 = x2 - int(self.corner_radius * max(self.upper_inner_radius_x, self.lower_inner_radius_x))
        y3 = y1 + int(self.corner_radius * self.upper_inner_radius_y)
        x4 = x2
        y4 = y2 - int(self.corner_radius * self.lower_inner_radius_y)
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_upper_rect(self, draw: ImageDraw, x1: int, y1: int, x2: int) -> None:
        x3 = x1 + int(self.corner_radius * self.upper_outer_radius_x)
        y3 = y1
        x4 = x2 - int(self.corner_radius * self.upper_inner_radius_x)
        y4 = y1 + int(self.corner_radius * max(self.upper_outer_radius_y, self.upper_inner_radius_y))
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_outer_rect(self, draw: ImageDraw, x1: int, y1: int, y2: int) -> None:
        x3 = x1
        y3 = y1 + int(self.corner_radius * self.upper_outer_radius_y)
        x4 = x1 + int(self.corner_radius * max(self.upper_outer_radius_x, self.lower_outer_radius_x))
        y4 = y2 - int(self.corner_radius * self.lower_outer_radius_y)
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_lower_rect(self, draw: ImageDraw, x1: int, x2: int, y2: int) -> None:
        x3 = x1 + int(self.corner_radius * self.lower_outer_radius_x)
        y3 = y2 - int(self.corner_radius * max(self.lower_outer_radius_y, self.lower_inner_radius_y))
        x4 = x2 - int(self.corner_radius * self.lower_inner_radius_x)
        y4 = y2
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_center_rect(self, draw: ImageDraw, x1: int, y1: int, x2: int, y2: int) -> None:
        x3 = x1 + int(self.corner_radius * max(self.upper_outer_radius_x, self.lower_outer_radius_x))
        y3 = y1 + int(self.corner_radius * max(self.upper_outer_radius_y, self.upper_inner_radius_y))
        x4 = x2 - int(self.corner_radius * max(self.upper_inner_radius_y, self.lower_inner_radius_y))
        y4 = y2 - int(self.corner_radius * max(self.lower_outer_radius_y, self.lower_inner_radius_y))
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_lower_inner_pie(self, draw: ImageDraw, x2: int, y2: int) -> None:
        x3 = x2 - 2 * int(self.corner_radius * self.lower_inner_radius_x)
        y3 = y2 - 2 * int(self.corner_radius * self.lower_inner_radius_y)
        x4 = x2
        y4 = y2
        draw.pieslice(((x3, y3), (x4, y4)), 0, 90, fill=1)

    def _render_upper_inner_pie(self, draw: ImageDraw, y1: int, x2: int) -> None:
        x3 = x2 - 2 * int(self.corner_radius * self.upper_inner_radius_x)
        y3 = y1
        x4 = x2
        y4 = y1 + 2 * int(self.corner_radius * self.upper_inner_radius_y)
        draw.pieslice(((x3, y3), (x4, y4)), 270, 360, fill=1)

    def _render_upper_outer_pie(self, draw: ImageDraw, x1: int, y1: int) -> None:
        x3 = x1
        y3 = y1
        x4 = x1 + 2 * int(self.corner_radius * self.upper_outer_radius_x)
        y4 = y1 + 2 * int(self.corner_radius * self.upper_outer_radius_y)
        draw.pieslice(((x3, y3), (x4, y4)), 180, 270, fill=1)

    def _render_lower_outer_pie(self, draw: ImageDraw, x1: int, y2: int) -> None:
        x3 = x1
        y3 = y2 - 2 * int(self.corner_radius * self.lower_outer_radius_y)
        x4 = x1 + 2 * int(self.corner_radius * self.lower_outer_radius_x)
        y4 = y2
        draw.pieslice(((x3, y3), (x4, y4)), 90, 180, fill=1)

    def render(self, im: Image) -> None:
        # Eye image
        eye = Image.new("1", (self.width, self.height), color=0)

        draw = ImageDraw.Draw(eye)
        x1 = eye.size[0] // 2 - self.half_eye_width
        y1 = eye.size[1] // 2 - self.half_eye_height
        x2 = eye.size[0] // 2 + self.half_eye_width
        y2 = eye.size[1] // 2 + self.half_eye_height
        self._render_inner_rect(draw, y1, x2, y2)
        self._render_upper_rect(draw, x1, y1, x2)
        self._render_outer_rect(draw, x1, y1, y2)
        self._render_lower_rect(draw, x1, x2, y2)
        self._render_center_rect(draw, x1, y1, x2, y2)
        self._render_lower_inner_pie(draw, x2, y2)
        self._render_upper_inner_pie(draw, y1, x2)
        self._render_upper_outer_pie(draw, x1, y1)
        self._render_lower_outer_pie(draw, x1, y2)

        # Draw lids
        self.lids[0].render(eye)
        self.lids[1].render(eye)

        # Rotate
        eye = eye.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(eye.size[0]) * self.scale_x),
                 int(float(eye.size[1]) * self.scale_y))
        try:
            eye = eye.resize(scale, resample=RESAMPLE)
        except ValueError:
            # Scale factors can be extremely small and Pillow cannot handle resize() with both scale factors of 0.
            eye = None

        # Translate and compose
        if eye:
            location = ((im.size[0] - eye.size[0]) // 2 + int(self.center_x * self.x_factor) + self.offset,
                        (im.size[1] - eye.size[1]) // 2 + int(self.center_y * self.y_factor))
            im.paste(eye, location, eye)


class ProceduralFace(ProceduralBase):

    X_FACTOR = 0.55
    Y_FACTOR = 0.25

    def __init__(self,
                 center_x: int = 0,
                 center_y: int = 0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 angle: float = 0.0,
                 left_eye: Optional[List] = None,
                 right_eye: Optional[List] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super(ProceduralFace, self).__init__(width, height)
        self.left_eye_offset = -int(self.width / 6)
        self.right_eye_offset = int(self.width / 6)
        self.center_x = int(center_x)
        self.center_y = int(center_y)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.angle = float(angle)
        if left_eye:
            self.left_eye = ProceduralEye(
                self.left_eye_offset,
                left_eye[0], left_eye[1],
                left_eye[2], left_eye[3],
                left_eye[4],
                left_eye[5], left_eye[6],
                left_eye[7], left_eye[8],
                left_eye[9], left_eye[10],
                left_eye[11], left_eye[12],
                left_eye[13], left_eye[14], left_eye[15],
                left_eye[16], left_eye[17], left_eye[18],
                width=self.width,
                height=self.height
            )
        else:
            self.left_eye = ProceduralEye(self.left_eye_offset)
        if right_eye:
            self.right_eye = ProceduralEye(
                self.right_eye_offset,
                right_eye[0], right_eye[1],
                right_eye[2], right_eye[3],
                right_eye[4],
                right_eye[5], right_eye[6],
                right_eye[7], right_eye[8],
                right_eye[9], right_eye[10],
                right_eye[11], right_eye[12],
                right_eye[13], right_eye[14], right_eye[15],
                right_eye[16], right_eye[17], right_eye[18],
                width=self.width,
                height=self.height
            )
        else:
            self.right_eye = ProceduralEye(self.right_eye_offset)

    def render(self) -> Image:
        # Background image
        im = Image.new("1", (self.width, self.height), color=0)

        # Face image
        face = Image.new("1", (self.width, self.height), color=0)

        # Draw eyes
        self.left_eye.render(face)
        self.right_eye.render(face)

        # Rotate
        face = face.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(face.size[0]) * self.scale_x),
                 int(float(face.size[1] * self.scale_y)))
        try:
            face = face.resize(scale, resample=RESAMPLE)
        except ValueError:
            # Scale factors can be extremely small and Pillow cannot handle resize() with both scale factors of 0.
            face = None

        # Translate and compose
        if face:
            location = ((im.size[0] - face.size[0]) // 2 + int(self.center_x * self.X_FACTOR),
                        (im.size[1] - face.size[1]) // 2 + int(self.center_y * self.Y_FACTOR))
            im.paste(face, location)

        return im

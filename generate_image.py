from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_post_image(text):

    img = Image.new(
        "RGB",
        (1080,1080),
        color=(18,18,40)
    )

    draw = ImageDraw.Draw(img)

    try:
        font=ImageFont.truetype(
            "arial.ttf",
            52
        )
    except:
        font=ImageFont.load_default()

    wrapped="\n".join(
        textwrap.wrap(
            text[:180],
            width=28
        )
    )

    draw.text(
        (120,250),
        wrapped,
        fill="white",
        font=font,
        spacing=20
    )

    draw.text(
        (120,900),
        "AI Social Media Generator",
        fill="#00E5FF",
        font=font
    )

    img.save("post_image.jpg")
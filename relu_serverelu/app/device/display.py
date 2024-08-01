from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.core.render import canvas
import asyncio

def setup_device(num_matrices=4, block_orientation=-90, rotate=0):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=num_matrices, block_orientation=block_orientation,
                     rotate=rotate, blocks_arranged_in_reverse_order=False)
    device.contrast(5)
    return device

device = setup_device()

def display_static_message(msg="Nimic"):
    with canvas(device) as draw:
        text(draw, (0, 0), msg, fill="white", font=proportional(LCD_FONT))

async def scroll_message(msg):
    width = device.width
    start_position = width
    while start_position > -len(msg) * 8:
        with canvas(device) as draw:
            text(draw, (start_position, 0), msg, fill="white", font=proportional(LCD_FONT))
        start_position -= 1
        await asyncio.sleep(0.15)

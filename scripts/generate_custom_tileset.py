from PIL import Image

# 8 columns x 14 rows of 32x32 tiles = 256 x 448 px
W, H = 256, 448
sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))

def draw_scaled_pixel(img, x0, y0, gx, gy, color):
    """Draw a 2x2 pixel block (authentic 2x GBA/RPG Maker XP scale) at (x0 + gx*2, y0 + gy*2)."""
    if color is None:
        return
    px = img.load()
    for dy in range(2):
        for dx in range(2):
            ix, iy = x0 + gx*2 + dx, y0 + gy*2 + dy
            if 0 <= ix < img.width and 0 <= iy < img.height:
                px[ix, iy] = color

def draw_rect_2x(img, x0, y0, gx0, gy0, gw, gh, color):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            draw_scaled_pixel(img, x0, y0, gx, gy, color)

def draw_box_2x(img, x0, y0, gx0, gy0, gw, gh, fill, outline):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            if gx == gx0 or gx == gx0 + gw - 1 or gy == gy0 or gy == gy0 + gh - 1:
                draw_scaled_pixel(img, x0, y0, gx, gy, outline)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, fill)

# Palette matching Interior_general.png & imgur_RriSFxo.png
OUTLINE = (56, 56, 72, 255)
SHADOW  = (0, 0, 0, 55)

# Silver/Grey Washing Machine Palette
WM_TOP_LIGHT = (228, 232, 240, 255)
WM_TOP_MID   = (200, 206, 216, 255)
WM_FRONT     = (172, 180, 192, 255)
WM_DARK      = (136, 144, 158, 255)
WM_PANEL     = (64, 72, 88, 255)
WM_GLASS_OUT = (80, 104, 128, 255)
WM_GLASS_IN  = (120, 168, 200, 255)
WM_GLASS_HI  = (200, 232, 248, 255)
WM_BTN_GREEN = (88, 216, 120, 255)
WM_BTN_RED   = (232, 88, 88, 255)

# White Washing Machine Palette
WW_TOP_LIGHT = (248, 248, 252, 255)
WW_TOP_MID   = (232, 236, 244, 255)
WW_FRONT     = (208, 214, 224, 255)
WW_DARK      = (168, 176, 188, 255)

# ==============================================================================
# 1. WASHING MACHINE (Top-Load & Front-Load, 4 Directions, 1x2 tiles = 32x64 px)
# ==============================================================================
# Cols 0..3, Rows 0..1: Silver LG Top-Loader (matching user's photo yellow_kitchen_laundry.jpg)
#   Col 0: Facing South (Down)
#   Col 1: Facing North (Up / Back)
#   Col 2: Facing East  (Right)
#   Col 3: Facing West  (Left)
# Cols 4..7, Rows 0..1: White Front-Loader / Top-Loader combo (4 directions)

def make_washer(x0, y0, direction, pal):
    top_l, top_m, front, dark = pal
    # Soft floor shadow at bottom
    draw_rect_2x(sheet, x0, y0, 1, 29, 14, 2, SHADOW)
    if direction == 'S':
        # Main body (gx=1..14, gy=6..29) -> 28x48 px
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 24, front, OUTLINE)
        # Top surface (gy=6..17)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 12, top_l, OUTLINE)
        # Back control panel raised ridge at gy=6..9
        draw_rect_2x(sheet, x0, y0, 2, 7, 12, 2, WM_PANEL)
        draw_scaled_pixel(sheet, x0, y0, 4, 7, WM_BTN_GREEN)
        draw_scaled_pixel(sheet, x0, y0, 6, 7, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 11, 7, WM_BTN_RED)
        # Top-loading glass window lid (gx=3..12, gy=10..15)
        draw_box_2x(sheet, x0, y0, 3, 10, 10, 6, WM_GLASS_IN, WM_GLASS_OUT)
        draw_scaled_pixel(sheet, x0, y0, 5, 11, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 6, 12, WM_GLASS_HI)
        # Front face details (gy=18..28)
        draw_rect_2x(sheet, x0, y0, 2, 18, 12, 1, top_m)
        # Yellow energy sticker on front left (like in user's photo!)
        draw_rect_2x(sheet, x0, y0, 3, 20, 3, 4, (248, 216, 56, 255))
        draw_rect_2x(sheet, x0, y0, 3, 20, 3, 1, (56, 120, 200, 255))
        # Bottom kickplate line
        draw_rect_2x(sheet, x0, y0, 2, 27, 12, 1, dark)
    elif direction == 'N':
        # Facing North (back of washer visible on south face, control panel on south edge of top)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 24, dark, OUTLINE)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 12, top_l, OUTLINE)
        # Glass lid towards north (gy=7..12)
        draw_box_2x(sheet, x0, y0, 3, 7, 10, 6, WM_GLASS_IN, WM_GLASS_OUT)
        draw_scaled_pixel(sheet, x0, y0, 5, 8, WM_GLASS_HI)
        # Control panel towards south edge of top (gy=14..16)
        draw_rect_2x(sheet, x0, y0, 2, 14, 12, 2, WM_PANEL)
        draw_scaled_pixel(sheet, x0, y0, 4, 14, WM_BTN_GREEN)
        draw_scaled_pixel(sheet, x0, y0, 11, 14, WM_BTN_RED)
        # Back service panel vents on visible south face
        draw_box_2x(sheet, x0, y0, 4, 20, 8, 6, front, dark)
    elif direction == 'E':
        # Facing East (Right): control panel on left (west) edge, glass lid on right (east)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 24, front, OUTLINE)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 12, top_l, OUTLINE)
        # Left raised control panel (gx=2..4, gy=7..16)
        draw_rect_2x(sheet, x0, y0, 2, 7, 3, 9, WM_PANEL)
        draw_scaled_pixel(sheet, x0, y0, 3, 9, WM_BTN_GREEN)
        draw_scaled_pixel(sheet, x0, y0, 3, 11, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 3, 14, WM_BTN_RED)
        # Glass lid to the right (gx=6..12, gy=8..15)
        draw_box_2x(sheet, x0, y0, 6, 8, 7, 8, WM_GLASS_IN, WM_GLASS_OUT)
        draw_scaled_pixel(sheet, x0, y0, 8, 10, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 9, 11, WM_GLASS_HI)
        # Side panel groove on south visible face
        draw_rect_2x(sheet, x0, y0, 3, 20, 10, 7, top_m)
        draw_rect_2x(sheet, x0, y0, 2, 27, 12, 1, dark)
    elif direction == 'W':
        # Facing West (Left): control panel on right (east) edge, glass lid on left (west)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 24, front, OUTLINE)
        draw_box_2x(sheet, x0, y0, 1, 6, 14, 12, top_l, OUTLINE)
        # Right raised control panel (gx=11..13, gy=7..16)
        draw_rect_2x(sheet, x0, y0, 11, 7, 3, 9, WM_PANEL)
        draw_scaled_pixel(sheet, x0, y0, 12, 9, WM_BTN_GREEN)
        draw_scaled_pixel(sheet, x0, y0, 12, 11, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 12, 14, WM_BTN_RED)
        # Glass lid to the left (gx=3..9, gy=8..15)
        draw_box_2x(sheet, x0, y0, 3, 8, 7, 8, WM_GLASS_IN, WM_GLASS_OUT)
        draw_scaled_pixel(sheet, x0, y0, 5, 10, WM_GLASS_HI)
        draw_scaled_pixel(sheet, x0, y0, 6, 11, WM_GLASS_HI)
        # Side panel groove on south visible face
        draw_rect_2x(sheet, x0, y0, 3, 20, 10, 7, top_m)
        draw_rect_2x(sheet, x0, y0, 2, 27, 12, 1, dark)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_washer(idx*32, 0, d, (WM_TOP_LIGHT, WM_TOP_MID, WM_FRONT, WM_DARK))
    make_washer((idx+4)*32, 0, d, (WW_TOP_LIGHT, WW_TOP_MID, WW_FRONT, WW_DARK))

# ==============================================================================
# 2. CAT LITTER BOX (Covered Blue/White Hooded Box + Open Tray, 4 Directions)
# ==============================================================================
# Rows 2..3 (y=64..128):
#   Row 2, Cols 0..3: Covered Blue & White Cat Litter Box (matching user's photo!) (S, N, E, W)
#   Row 3, Cols 0..3: Open Cat Litter Tray with Sandy Litter (S, N, E, W)
#   Row 2..3, Cols 4..7: Tall 1x2 Litter Box + Mat variants

LB_WHITE = (244, 246, 250, 255)
LB_SHADE = (212, 218, 228, 255)
LB_BLUE  = (56, 96, 176, 255)
LB_BLUE_D= (36, 68, 136, 255)
LB_DOOR  = (64, 68, 84, 255)
SAND_L   = (224, 200, 152, 255)
SAND_D   = (192, 168, 120, 255)

def make_litter_box_hooded(x0, y0, direction):
    draw_rect_2x(sheet, x0, y0, 2, 13, 12, 2, SHADOW)
    # Blue lower tray (gy=8..13)
    draw_box_2x(sheet, x0, y0, 2, 8, 12, 6, LB_BLUE, OUTLINE)
    # White upper hood (gy=2..9)
    draw_box_2x(sheet, x0, y0, 2, 2, 12, 7, LB_WHITE, OUTLINE)
    draw_rect_2x(sheet, x0, y0, 3, 7, 10, 1, LB_SHADE)
    # Top handle/vent on hood
    draw_rect_2x(sheet, x0, y0, 6, 3, 4, 1, LB_BLUE)
    if direction == 'S':
        # Dark entry flap on front (south) face
        draw_box_2x(sheet, x0, y0, 5, 6, 6, 6, LB_DOOR, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 7, 4, 1, LB_SHADE)
    elif direction == 'N':
        # Entry on north side (indicated by notch at top edge), solid back facing south
        draw_rect_2x(sheet, x0, y0, 5, 2, 6, 1, LB_DOOR)
    elif direction == 'E':
        # Entry on right (east) side
        draw_box_2x(sheet, x0, y0, 10, 5, 4, 6, LB_DOOR, OUTLINE)
    elif direction == 'W':
        # Entry on left (west) side
        draw_box_2x(sheet, x0, y0, 2, 5, 4, 6, LB_DOOR, OUTLINE)

def make_litter_box_open(x0, y0, direction):
    draw_rect_2x(sheet, x0, y0, 2, 13, 12, 2, SHADOW)
    if direction in ('S', 'N'):
        draw_box_2x(sheet, x0, y0, 2, 3, 12, 11, LB_BLUE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 3, 4, 10, 7, SAND_L, OUTLINE)
        draw_scaled_pixel(sheet, x0, y0, 5, 6, SAND_D)
        draw_scaled_pixel(sheet, x0, y0, 9, 8, SAND_D)
        draw_scaled_pixel(sheet, x0, y0, 7, 5, SAND_D)
        # Scoop on side
        sx = 12 if direction == 'S' else 3
        draw_rect_2x(sheet, x0, y0, sx, 5, 1, 4, LB_WHITE)
    else:
        draw_box_2x(sheet, x0, y0, 3, 2, 10, 12, LB_BLUE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 4, 3, 8, 8, SAND_L, OUTLINE)
        draw_scaled_pixel(sheet, x0, y0, 6, 5, SAND_D)
        draw_scaled_pixel(sheet, x0, y0, 8, 8, SAND_D)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_litter_box_hooded(idx*32, 2*32, d)
    make_litter_box_open(idx*32, 3*32, d)

# Also add Cat Food & Water Bowls in Row 2..3, Cols 4..7 (4 orientations!)
BOWL_RED  = (224, 72, 64, 255)
BOWL_BLUE = (64, 152, 224, 255)
WATER_COL = (136, 208, 248, 255)
FOOD_COL  = (160, 96, 56, 255)

def make_cat_bowls(x0, y0, direction):
    if direction in ('S', 'N'):
        # Horizontal pair of bowls
        b1, b2 = (BOWL_RED, FOOD_COL) if direction == 'S' else (BOWL_BLUE, WATER_COL)
        c1, c2 = (BOWL_BLUE, WATER_COL) if direction == 'S' else (BOWL_RED, FOOD_COL)
        draw_box_2x(sheet, x0, y0, 1, 6, 6, 5, b1, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 2, 7, 4, 2, b2)
        draw_box_2x(sheet, x0, y0, 9, 6, 6, 5, c1, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 10, 7, 4, 2, c2)
    else:
        # Vertical pair of bowls
        b1, b2 = (BOWL_RED, FOOD_COL) if direction == 'E' else (BOWL_BLUE, WATER_COL)
        c1, c2 = (BOWL_BLUE, WATER_COL) if direction == 'E' else (BOWL_RED, FOOD_COL)
        draw_box_2x(sheet, x0, y0, 5, 1, 6, 5, b1, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 2, 4, 2, b2)
        draw_box_2x(sheet, x0, y0, 5, 9, 6, 5, c1, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 10, 4, 2, c2)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_cat_bowls((idx+4)*32, 2*32, d)

# ==============================================================================
# 3. MOP & RED MOP BUCKET (4 Directions, Rows 4..5 for 1x2 Mop+Bucket, Row 6 for 1x1 Bucket)
# ==============================================================================
# Rows 4..5, Cols 0..3: Red Mop Bucket with Mop Stick Leaning in 4 Directions (S, N, E, W) (1x2 tiles = 32x64)
# Rows 4..5, Cols 4..7: Standalone Mop (S, N, E, W) (1x2 tiles = 32x64)
# Row 6, Cols 0..3: Compact 1x1 Red Mop Bucket with Wringer in 4 Directions (S, N, E, W) (32x32)

RED_LIGHT = (240, 72, 64, 255)
RED_MID   = (204, 44, 40, 255)
RED_DARK  = (156, 28, 28, 255)
MOP_HEAD  = (232, 228, 212, 255)
MOP_SHADE = (196, 188, 168, 255)
STICK_COL = (184, 40, 40, 255)
GREEN_RAG = (40, 144, 72, 255) # green cloth in bucket from user's photo!

def make_mop_and_bucket_1x2(x0, y0, direction):
    # Bucket sits in lower tile (gy=16..30)
    draw_rect_2x(sheet, x0, y0, 3, 29, 10, 2, SHADOW)
    draw_box_2x(sheet, x0, y0, 3, 20, 10, 10, RED_MID, OUTLINE)
    draw_box_2x(sheet, x0, y0, 2, 17, 12, 5, RED_LIGHT, OUTLINE)
    # Inside bucket rim
    draw_rect_2x(sheet, x0, y0, 4, 18, 8, 2, RED_DARK)
    # Green cloth / mop head inside bucket
    if direction == 'S':
        draw_rect_2x(sheet, x0, y0, 5, 18, 5, 2, GREEN_RAG)
        # Mop handle rising straight up from center-right
        draw_rect_2x(sheet, x0, y0, 9, 3, 2, 16, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 9, 4, 1, 15, STICK_COL)
        draw_box_2x(sheet, x0, y0, 6, 17, 6, 3, MOP_HEAD, OUTLINE)
    elif direction == 'N':
        draw_rect_2x(sheet, x0, y0, 6, 18, 5, 2, GREEN_RAG)
        draw_rect_2x(sheet, x0, y0, 6, 3, 2, 16, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 4, 1, 15, STICK_COL)
        draw_box_2x(sheet, x0, y0, 5, 16, 6, 3, MOP_HEAD, OUTLINE)
    elif direction == 'E':
        # Handle leaning slightly from left to right, wringer on right
        draw_box_2x(sheet, x0, y0, 8, 16, 5, 4, MOP_HEAD, OUTLINE)
        for gy in range(4, 18):
            gx = 5 + (gy - 4) // 4
            draw_scaled_pixel(sheet, x0, y0, gx, gy, STICK_COL)
            draw_scaled_pixel(sheet, x0, y0, gx+1, gy, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 4, 18, 4, 2, GREEN_RAG)
    elif direction == 'W':
        # Handle leaning from right to left, wringer on left
        draw_box_2x(sheet, x0, y0, 3, 16, 5, 4, MOP_HEAD, OUTLINE)
        for gy in range(4, 18):
            gx = 10 - (gy - 4) // 4
            draw_scaled_pixel(sheet, x0, y0, gx, gy, STICK_COL)
            draw_scaled_pixel(sheet, x0, y0, gx-1, gy, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 8, 18, 4, 2, GREEN_RAG)

def make_standalone_mop_1x2(x0, y0, direction):
    draw_rect_2x(sheet, x0, y0, 4, 28, 8, 2, SHADOW)
    if direction in ('S', 'N'):
        # Vertical stick + mop head at bottom
        draw_rect_2x(sheet, x0, y0, 7, 3, 2, 22, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 7, 4, 1, 20, STICK_COL)
        draw_box_2x(sheet, x0, y0, 4, 24, 8, 5, MOP_HEAD, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, 27, 6, 1, MOP_SHADE)
    elif direction == 'E':
        draw_rect_2x(sheet, x0, y0, 6, 3, 2, 22, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 4, 1, 20, STICK_COL)
        draw_box_2x(sheet, x0, y0, 5, 23, 7, 6, MOP_HEAD, OUTLINE)
    elif direction == 'W':
        draw_rect_2x(sheet, x0, y0, 8, 3, 2, 22, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 8, 4, 1, 20, STICK_COL)
        draw_box_2x(sheet, x0, y0, 4, 23, 7, 6, MOP_HEAD, OUTLINE)

def make_bucket_1x1(x0, y0, direction):
    draw_rect_2x(sheet, x0, y0, 3, 13, 10, 2, SHADOW)
    draw_box_2x(sheet, x0, y0, 3, 5, 10, 9, RED_MID, OUTLINE)
    draw_box_2x(sheet, x0, y0, 2, 3, 12, 4, RED_LIGHT, OUTLINE)
    draw_rect_2x(sheet, x0, y0, 4, 4, 8, 2, RED_DARK)
    if direction == 'S':
        draw_rect_2x(sheet, x0, y0, 5, 4, 5, 2, GREEN_RAG)
    elif direction == 'N':
        draw_rect_2x(sheet, x0, y0, 6, 3, 5, 2, GREEN_RAG)
    elif direction == 'E':
        draw_rect_2x(sheet, x0, y0, 7, 4, 4, 2, GREEN_RAG)
    elif direction == 'W':
        draw_rect_2x(sheet, x0, y0, 4, 4, 4, 2, GREEN_RAG)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_mop_and_bucket_1x2(idx*32, 4*32, d)
    make_standalone_mop_1x2((idx+4)*32, 4*32, d)
    make_bucket_1x1(idx*32, 6*32, d)

# ==============================================================================
# 4. CAT SPRITES (Calico Cat from user's photos + Sleeping/Sitting variants, 4 Directions)
# ==============================================================================
# Row 7, Cols 0..3: Calico Cat Sitting/Standing in 4 Directions (S, N, E, W) (32x32)
# Row 7, Cols 4..7: Calico Cat Walking/Eating in 4 Directions (S, N, E, W) (32x32)
# Row 8, Cols 0..3: Calico Cat Curled/Sleeping in 4 Directions (S, N, E, W) (32x32)

CAT_WHITE  = (248, 248, 252, 255)
CAT_SHADE  = (216, 220, 228, 255)
CAT_ORANGE = (224, 136, 56, 255)
CAT_DARK   = (64, 56, 56, 255)
CAT_EYE    = (40, 48, 40, 255)
CAT_NOSE   = (232, 136, 152, 255)

def make_cat(x0, y0, direction, pose='sit'):
    draw_rect_2x(sheet, x0, y0, 4, 12, 8, 2, SHADOW)
    if direction == 'S':
        # Body (gx=5..10, gy=7..12)
        draw_box_2x(sheet, x0, y0, 4, 7, 8, 6, CAT_WHITE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, 8, 2, 3, CAT_ORANGE)
        draw_rect_2x(sheet, x0, y0, 9, 8, 2, 2, CAT_DARK)
        # Head (gx=4..11, gy=2..8)
        draw_box_2x(sheet, x0, y0, 4, 2, 8, 6, CAT_WHITE, OUTLINE)
        # Ears
        draw_box_2x(sheet, x0, y0, 4, 1, 3, 2, CAT_ORANGE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 9, 1, 3, 2, CAT_DARK, OUTLINE)
        # Patches on forehead
        draw_rect_2x(sheet, x0, y0, 5, 3, 2, 1, CAT_ORANGE)
        draw_rect_2x(sheet, x0, y0, 9, 3, 2, 1, CAT_DARK)
        # Eyes & Pink Nose
        draw_scaled_pixel(sheet, x0, y0, 6, 5, CAT_EYE)
        draw_scaled_pixel(sheet, x0, y0, 9, 5, CAT_EYE)
        draw_scaled_pixel(sheet, x0, y0, 7, 6, CAT_NOSE)
        # Tail sticking out to the right
        draw_box_2x(sheet, x0, y0, 11, 9, 3, 2, CAT_ORANGE, OUTLINE)
    elif direction == 'N':
        # Back of cat facing North
        draw_box_2x(sheet, x0, y0, 4, 6, 8, 7, CAT_WHITE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, 7, 3, 3, CAT_ORANGE)
        draw_rect_2x(sheet, x0, y0, 8, 8, 3, 3, CAT_DARK)
        # Head from behind
        draw_box_2x(sheet, x0, y0, 4, 2, 8, 5, CAT_WHITE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 4, 1, 3, 2, CAT_DARK, OUTLINE)
        draw_box_2x(sheet, x0, y0, 9, 1, 3, 2, CAT_ORANGE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, 3, 2, 2, CAT_DARK)
        draw_rect_2x(sheet, x0, y0, 8, 3, 3, 2, CAT_ORANGE)
        # Upright tail in front (south)
        draw_box_2x(sheet, x0, y0, 7, 9, 2, 5, CAT_ORANGE, OUTLINE)
        draw_scaled_pixel(sheet, x0, y0, 7, 9, CAT_DARK)
    elif direction == 'E':
        # Side profile facing East (Right)
        # Body (gx=3..11, gy=6..12)
        draw_box_2x(sheet, x0, y0, 3, 6, 8, 6, CAT_WHITE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 4, 7, 3, 3, CAT_DARK)
        draw_rect_2x(sheet, x0, y0, 7, 7, 2, 2, CAT_ORANGE)
        # Head on right (gx=8..14, gy=3..9)
        hy = 4 if pose == 'eat' else 2
        draw_box_2x(sheet, x0, y0, 8, hy, 6, 6, CAT_WHITE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 9, hy-1, 3, 2, CAT_ORANGE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 9, hy+1, 2, 2, CAT_ORANGE)
        draw_scaled_pixel(sheet, x0, y0, 12, hy+3, CAT_EYE)
        draw_scaled_pixel(sheet, x0, y0, 13, hy+4, CAT_NOSE)
        # Tail on left (gx=1..4, gy=5..9)
        draw_box_2x(sheet, x0, y0, 1, 5, 3, 3, CAT_ORANGE, OUTLINE)
    elif direction == 'W':
        # Side profile facing West (Left)
        # Body (gx=5..13, gy=6..12)
        draw_box_2x(sheet, x0, y0, 5, 6, 8, 6, CAT_WHITE, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 9, 7, 3, 3, CAT_DARK)
        draw_rect_2x(sheet, x0, y0, 7, 7, 2, 2, CAT_ORANGE)
        # Head on left (gx=2..8, gy=3..9)
        hy = 4 if pose == 'eat' else 2
        draw_box_2x(sheet, x0, y0, 2, hy, 6, 6, CAT_WHITE, OUTLINE)
        draw_box_2x(sheet, x0, y0, 4, hy-1, 3, 2, CAT_DARK, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, hy+1, 2, 2, CAT_ORANGE)
        draw_scaled_pixel(sheet, x0, y0, 3, hy+3, CAT_EYE)
        draw_scaled_pixel(sheet, x0, y0, 2, hy+4, CAT_NOSE)
        # Tail on right (gx=12..15, gy=5..9)
        draw_box_2x(sheet, x0, y0, 12, 5, 3, 3, CAT_ORANGE, OUTLINE)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_cat(idx*32, 7*32, d, pose='sit')
    make_cat((idx+4)*32, 7*32, d, pose='eat')

# Sleeping curled cat in Row 8, Cols 0..3
for idx, d in enumerate(['S', 'N', 'E', 'W']):
    x0, y0 = idx*32, 8*32
    draw_rect_2x(sheet, x0, y0, 3, 11, 10, 2, SHADOW)
    draw_box_2x(sheet, x0, y0, 3, 5, 10, 7, CAT_WHITE, OUTLINE)
    draw_rect_2x(sheet, x0, y0, 4, 6, 3, 3, CAT_ORANGE)
    draw_rect_2x(sheet, x0, y0, 8, 6, 3, 3, CAT_DARK)
    hx = 4 if d in ('W', 'S') else 8
    draw_box_2x(sheet, x0, y0, hx, 6, 4, 4, CAT_WHITE, OUTLINE)
    draw_scaled_pixel(sheet, x0, y0, hx+1, 7, CAT_ORANGE)

sheet.save('tilesets/custom_home_items.png')

# Also save a 2x zoomed preview with labels so the user can see every tile clearly!
preview = Image.new('RGBA', (W*2, H*2), (220, 224, 232, 255))
preview.alpha_composite(sheet.resize((W*2, H*2), Image.NEAREST))
preview.save('/tmp/custom_home_items_preview.png')
print('Generated custom_home_items.png successfully!')

# ==============================================================================
# 5. XIAOMI MIJIA 1C ROBOT VACUUM ("Robotina") + CHARGING DOCK (4 Directions)
# ==============================================================================
# Row 9, Cols 0..3: Xiaomi Mijia 1C Robot Vacuum (Standalone, 4 Directions: S, N, E, W)
# Row 9, Cols 4..7: Xiaomi Mijia 1C Charging Dock (Standalone, 4 Directions: S, N, E, W)
# Row 10, Cols 0..3: Xiaomi Mijia 1C Docked on Charging Base (Combined 1x1, 4 Directions: S, N, E, W)

VAC_WHITE  = (248, 250, 252, 255)
VAC_LIGHT  = (232, 236, 242, 255)
VAC_SHADE  = (196, 204, 216, 255)
VAC_BUMPER = (64, 68, 80, 255)
VAC_SENSOR = (36, 40, 52, 255)
VAC_LED    = (88, 208, 248, 255)
DOCK_BODY  = (236, 240, 246, 255)
DOCK_WIN   = (32, 36, 44, 255)

def make_mijia_1c(x0, y0, direction, with_dock=False):
    # Floor shadow under round robot
    draw_rect_2x(sheet, x0, y0, 3, 13, 10, 2, SHADOW)
    if with_dock:
        if direction == 'S': # Dock at top (north wall), robot docked facing south
            draw_box_2x(sheet, x0, y0, 4, 0, 8, 5, DOCK_BODY, OUTLINE)
            draw_rect_2x(sheet, x0, y0, 5, 2, 6, 2, DOCK_WIN)
        elif direction == 'N': # Dock at bottom (south wall), robot facing north
            draw_box_2x(sheet, x0, y0, 4, 11, 8, 5, DOCK_BODY, OUTLINE)
            draw_rect_2x(sheet, x0, y0, 5, 12, 6, 2, DOCK_WIN)
        elif direction == 'E': # Dock at left (west wall), robot facing east
            draw_box_2x(sheet, x0, y0, 0, 4, 5, 8, DOCK_BODY, OUTLINE)
            draw_rect_2x(sheet, x0, y0, 2, 5, 2, 6, DOCK_WIN)
        elif direction == 'W': # Dock at right (east wall), robot facing west
            draw_box_2x(sheet, x0, y0, 11, 4, 5, 8, DOCK_BODY, OUTLINE)
            draw_rect_2x(sheet, x0, y0, 12, 5, 2, 6, DOCK_WIN)

    # Round 16x16 grid circle (gx=2..13, gy=2..13 -> 24x24 px circular body)
    # Using classic Pokémon circular sprite mask:
    circle_rows = [
        (2, 5, 6),   # gy=2: gx=5..10
        (3, 3, 10),  # gy=3: gx=3..12
        (4, 3, 10),  # gy=4: gx=3..12
        (5, 2, 12),  # gy=5: gx=2..13
        (6, 2, 12),  # gy=6: gx=2..13
        (7, 2, 12),  # gy=7: gx=2..13
        (8, 2, 12),  # gy=8: gx=2..13
        (9, 2, 12),  # gy=9: gx=2..13
        (10, 2, 12), # gy=10: gx=2..13
        (11, 3, 10), # gy=11: gx=3..12
        (12, 3, 10), # gy=12: gx=3..12
        (13, 5, 6),  # gy=13: gx=5..10
    ]
    inside = set()
    for gy, gx0, gw in circle_rows:
        for gx in range(gx0, gx0 + gw):
            inside.add((gx, gy))

    for (gx, gy) in inside:
        # Check if border of circle
        is_border = any((gx+dx, gy+dy) not in inside for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])
        if is_border:
            draw_scaled_pixel(sheet, x0, y0, gx, gy, OUTLINE)
        else:
            # 3/4 top-down thickness shading on bottom edge (gy=11..12)
            if gy >= 11:
                draw_scaled_pixel(sheet, x0, y0, gx, gy, VAC_SHADE)
            elif gy == 10:
                draw_scaled_pixel(sheet, x0, y0, gx, gy, VAC_LIGHT)
            else:
                draw_scaled_pixel(sheet, x0, y0, gx, gy, VAC_WHITE)

    # Inner ring line details & Mijia 1C VSLAM camera + power/home button strip
    if direction == 'S':
        # Front bumper dark strip at bottom (south)
        for gx in range(5, 11):
            draw_scaled_pixel(sheet, x0, y0, gx, 12, VAC_BUMPER)
        # VSLAM optical camera window (small dark square near front-center)
        draw_rect_2x(sheet, x0, y0, 7, 9, 2, 2, VAC_SENSOR)
        # Power/Home button pill near back-center with cyan LED
        draw_rect_2x(sheet, x0, y0, 7, 5, 2, 3, VAC_SHADE)
        draw_scaled_pixel(sheet, x0, y0, 7, 6, VAC_LED)
    elif direction == 'N':
        # Front bumper dark strip at top (north)
        for gx in range(5, 11):
            draw_scaled_pixel(sheet, x0, y0, gx, 3, VAC_BUMPER)
        # VSLAM optical camera window near north-center
        draw_rect_2x(sheet, x0, y0, 7, 5, 2, 2, VAC_SENSOR)
        # Power/Home button pill near south-center
        draw_rect_2x(sheet, x0, y0, 7, 8, 2, 3, VAC_SHADE)
        draw_scaled_pixel(sheet, x0, y0, 7, 9, VAC_LED)
    elif direction == 'E':
        # Front bumper dark strip on right (east)
        for gy in range(5, 11):
            draw_scaled_pixel(sheet, x0, y0, 12, gy, VAC_BUMPER)
        # VSLAM camera near east-center
        draw_rect_2x(sheet, x0, y0, 9, 7, 2, 2, VAC_SENSOR)
        # Power/Home button pill near west-center
        draw_rect_2x(sheet, x0, y0, 5, 7, 3, 2, VAC_SHADE)
        draw_scaled_pixel(sheet, x0, y0, 6, 7, VAC_LED)
    elif direction == 'W':
        # Front bumper dark strip on left (west)
        for gy in range(5, 11):
            draw_scaled_pixel(sheet, x0, y0, 3, gy, VAC_BUMPER)
        # VSLAM camera near west-center
        draw_rect_2x(sheet, x0, y0, 5, 7, 2, 2, VAC_SENSOR)
        # Power/Home button pill near east-center
        draw_rect_2x(sheet, x0, y0, 8, 7, 3, 2, VAC_SHADE)
        draw_scaled_pixel(sheet, x0, y0, 9, 7, VAC_LED)

def make_dock_only(x0, y0, direction):
    if direction == 'S': # Placed against north wall facing south
        draw_rect_2x(sheet, x0, y0, 4, 9, 8, 2, SHADOW)
        draw_box_2x(sheet, x0, y0, 4, 2, 8, 8, DOCK_BODY, OUTLINE)
        draw_box_2x(sheet, x0, y0, 5, 4, 6, 4, DOCK_WIN, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 6, 8, 4, 2, VAC_BUMPER)
    elif direction == 'N': # Placed against south wall facing north
        draw_rect_2x(sheet, x0, y0, 4, 13, 8, 2, SHADOW)
        draw_box_2x(sheet, x0, y0, 4, 6, 8, 8, DOCK_BODY, OUTLINE)
        draw_rect_2x(sheet, x0, y0, 5, 7, 6, 2, DOCK_WIN)
    elif direction == 'E': # Placed against west wall facing east
        draw_rect_2x(sheet, x0, y0, 2, 12, 6, 2, SHADOW)
        draw_box_2x(sheet, x0, y0, 2, 4, 6, 8, DOCK_BODY, OUTLINE)
        draw_box_2x(sheet, x0, y0, 5, 5, 3, 6, DOCK_WIN, OUTLINE)
    elif direction == 'W': # Placed against east wall facing west
        draw_rect_2x(sheet, x0, y0, 8, 12, 6, 2, SHADOW)
        draw_box_2x(sheet, x0, y0, 8, 4, 6, 8, DOCK_BODY, OUTLINE)
        draw_box_2x(sheet, x0, y0, 8, 5, 3, 6, DOCK_WIN, OUTLINE)

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_mijia_1c(idx*32, 9*32, d, with_dock=False)
    make_dock_only((idx+4)*32, 9*32, d)
    make_mijia_1c(idx*32, 10*32, d, with_dock=True)

sheet.save('tilesets/custom_home_items.png')
preview = Image.new('RGBA', (W*2, H*2), (220, 224, 232, 255))
preview.alpha_composite(sheet.resize((W*2, H*2), Image.NEAREST))
preview.save('/tmp/custom_home_items_preview.png')
print('Updated custom_home_items.png with Xiaomi Mijia 1C robot vacuum!')

# ==============================================================================
# 6. ASH / RED & MISTY OVERWORLD SPRITES (From Pokémon Essentials FRLG)
# ==============================================================================
# In RPG Maker XP / Pokémon Essentials, each character sheet is 128x192 (4 cols x 4 rows of 32x48 frames):
#   Row 0: Facing South (Down)  - Frame 0 is idle standing, Frame 1 is walking
#   Row 1: Facing West  (Left)  - Frame 0 is idle standing, Frame 1 is walking
#   Row 2: Facing East  (Right) - Frame 0 is idle standing, Frame 1 is walking
#   Row 3: Facing North (Up)    - Frame 0 is idle standing, Frame 1 is walking
# Let's place both:
# 1) 1x2 Full 32x48 Sprites in Rows 11..12 (y=352..416):
#    - Cols 0..3: Ash / Red (South, North, East, West)
#    - Cols 4..7: Misty     (South, North, East, West)
# 2) 1x1 Single-Tile 32x32 Sprites in Row 13 (y=416..448) (since each character's actual pixels are ~28x32!):
#    - Cols 0..3: Ash / Red (South, North, East, West) in a single 32x32 tile!
#    - Cols 4..7: Misty     (South, North, East, West) in a single 32x32 tile!

red_sheet = Image.open('/tmp/chars/trchar000.png').convert('RGBA')
misty_sheet = Image.open('/tmp/chars/trchar060.png').convert('RGBA')

# Map our standard (S, N, E, W) order to RPG Maker XP row indices (0=S, 3=N, 2=E, 1=W)
dir_to_rmxp_row = {'S': 0, 'N': 3, 'E': 2, 'W': 1}

def extract_char_frame(char_img, rmxp_row, col=0):
    frame = char_img.crop((col*32, rmxp_row*48, (col+1)*32, (rmxp_row+1)*48))
    # Find bounding box of non-transparent pixels
    bbox = frame.getbbox()
    return frame, bbox

for idx, d in enumerate(['S', 'N', 'E', 'W']):
    r_row = dir_to_rmxp_row[d]
    # Ash / Red
    red_f, red_bbox = extract_char_frame(red_sheet, r_row, 0)
    # Place in Rows 11..12 (1x2 tiles, bottom-aligned to Row 12)
    sheet.alpha_composite(red_f, (idx*32, 11*32 + 12))
    # Place in Row 13 (1x1 tile, cropped tightly around the 32px tall character body!)
    if red_bbox:
        top_y = max(0, red_bbox[1] - 1)
        red_1x1 = red_f.crop((0, top_y, 32, min(48, top_y + 32)))
        sheet.alpha_composite(red_1x1, (idx*32, 13*32 + (32 - red_1x1.height)))

    # Misty
    misty_f, misty_bbox = extract_char_frame(misty_sheet, r_row, 0)
    # Place in Rows 11..12 (Cols 4..7)
    sheet.alpha_composite(misty_f, ((idx+4)*32, 11*32 + 12))
    # Place in Row 13 (Cols 4..7, 1x1 tile)
    if misty_bbox:
        top_y = max(0, misty_bbox[1] - 1)
        misty_1x1 = misty_f.crop((0, top_y, 32, min(48, top_y + 32)))
        sheet.alpha_composite(misty_1x1, ((idx+4)*32, 13*32 + (32 - misty_1x1.height)))

sheet.save('tilesets/custom_home_items.png')

# Also save standalone transparent PNGs of Red & Misty in `ha_floorplan/` in case the user wants to use them as dynamic Home Assistant picture-elements overlays (e.g., person/room presence tracking)!
ha_dir = 'www'
for d in ['S', 'N', 'E', 'W']:
    r_row = dir_to_rmxp_row[d]
    rf, rbbox = extract_char_frame(red_sheet, r_row, 0)
    mf, mbbox = extract_char_frame(misty_sheet, r_row, 0)
    rf.crop((0, max(0, rbbox[1]-1), 32, min(48, max(0, rbbox[1]-1)+32))).save(f'{ha_dir}/red_{d.lower()}.png')
    mf.crop((0, max(0, mbbox[1]-1), 32, min(48, max(0, mbbox[1]-1)+32))).save(f'{ha_dir}/misty_{d.lower()}.png')

preview = Image.new('RGBA', (W*2, H*2), (220, 224, 232, 255))
preview.alpha_composite(sheet.resize((W*2, H*2), Image.NEAREST))
preview.save('/tmp/custom_home_items_preview.png')
print('Added Ash/Red and Misty to custom_home_items.png!')
from PIL import Image

# Load existinggenerate_custom_tileset.py logic by expanding canvas from 256x448 (14 rows) to 256x544 (17 rows)
old_sheet = Image.open('tilesets/custom_home_items.png').convert('RGBA')
W, H = 256, 544  # 8 cols x 17 rows of 32x32 tiles
sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sheet.paste(old_sheet.crop((0, 0, 256, 448)), (0, 0))

def draw_scaled_pixel(img, x0, y0, gx, gy, color):
    if color is None:
        return
    px = img.load()
    for dy in range(2):
        for dx in range(2):
            ix, iy = x0 + gx*2 + dx, y0 + gy*2 + dy
            if 0 <= ix < img.width and 0 <= iy < img.height:
                px[ix, iy] = color

def draw_rect_2x(img, x0, y0, gx0, gy0, gw, gh, color):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            draw_scaled_pixel(img, x0, y0, gx, gy, color)

def draw_box_2x(img, x0, y0, gx0, gy0, gw, gh, fill, outline):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            if gx == gx0 or gx == gx0 + gw - 1 or gy == gy0 or gy == gy0 + gh - 1:
                draw_scaled_pixel(img, x0, y0, gx, gy, outline)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, fill)

OUTLINE    = (48, 48, 64, 255)
SHADOW     = (0, 0, 0, 60)

# ==============================================================================
# 7. CHRISTMAS TREES (Rows 14..15, Cols 0..3 -> 1x2 tiles = 32x64 px)
#    Matches the exact height (gy=3..31) & pot placement of the Living Room plant!
# ==============================================================================
PINE_DARK  = (24, 88, 48, 255)
PINE_MID   = (40, 128, 64, 255)
PINE_LIGHT = (72, 168, 88, 255)
PINE_SNOW  = (232, 244, 252, 255)
TRUNK_DARK = (104, 64, 36, 255)
TRUNK_MID  = (136, 88, 48, 255)
POT_RED    = (192, 48, 48, 255)
POT_RED_L  = (224, 72, 64, 255)
POT_GOLD   = (248, 208, 64, 255)
STAR_GOLD  = (255, 232, 72, 255)
STAR_SHADE = (224, 168, 32, 255)
ORN_RED    = (240, 56, 56, 255)
ORN_BLUE   = (64, 160, 248, 255)
ORN_GOLD   = (255, 216, 64, 255)
ORN_PINK   = (248, 112, 184, 255)
GARLAND    = (248, 224, 112, 255)
LIGHT_GLOW = (255, 248, 168, 255)

def make_christmas_tree(img, x0, y0, variant=0):
    """
    variant 0: Classic Decorated Christmas Tree (1x2, fits standard living room plant)
    variant 1: Christmas Tree + Holiday Presents at base
    variant 2: Full-Mask Wide Christmas Tree (completely covers 100% of underlying living room plant pixels!)
    variant 3: Snowy / Extra-Lit Christmas Tree
    """
    # Floor shadow
    draw_rect_2x(img, x0, y0, 2, 30, 12, 2, SHADOW)

    # Festive Pot at bottom (gy=24..31, gx=3..12 -> covers the living room plant's pot at gx=3..12, gy=21..31!)
    draw_box_2x(img, x0, y0, 3, 24, 10, 7, POT_RED, OUTLINE)
    draw_rect_2x(img, x0, y0, 4, 25, 2, 5, POT_RED_L)
    # Pot Rim with Gold Trim (gy=22..24)
    draw_box_2x(img, x0, y0, 3, 22, 10, 3, POT_RED_L, OUTLINE)
    draw_rect_2x(img, x0, y0, 4, 23, 8, 1, POT_GOLD)

    # Tree Trunk (gy=20..22, gx=6..9)
    draw_box_2x(img, x0, y0, 5, 19, 6, 4, TRUNK_MID, OUTLINE)
    draw_rect_2x(img, x0, y0, 8, 20, 2, 2, TRUNK_DARK)

    # Tiered Pine Foliage (gy=5..21)
    # If variant == 2 (Full-Mask overlay over existing plant), widen upper/mid tiers by 1-2 px to cover every leaf of the plant underneath!
    if variant == 2:
        tiers = [
            (5, 6, 4),   # gy=5
            (6, 2, 12),  # gy=6
            (7, 2, 12),  # gy=7
            (8, 2, 12),  # gy=8
            (9, 2, 12),  # gy=9
            (10, 1, 14), # gy=10
            (11, 0, 16), # gy=11
            (12, 0, 16), # gy=12
            (13, 1, 14), # gy=13
            (14, 1, 14), # gy=14
            (15, 0, 16), # gy=15
            (16, 0, 16), # gy=16
            (17, 1, 14), # gy=17
            (18, 1, 14), # gy=18
            (19, 0, 16), # gy=19
            (20, 0, 16), # gy=20
            (21, 2, 12), # gy=21
        ]
    else:
        # Classic conical 4-tier pine silhouette (still same height gy=3..31!)
        tiers = [
            (5, 7, 2),   # Tip
            (6, 6, 4),
            (7, 5, 6),
            (8, 4, 8),   # Tier 1 bottom
            (9, 5, 6),   # Tier 2 top
            (10, 4, 8),
            (11, 3, 10),
            (12, 2, 12), # Tier 2 bottom
            (13, 4, 8),  # Tier 3 top
            (14, 3, 10),
            (15, 2, 12),
            (16, 1, 14), # Tier 3 bottom
            (17, 3, 10), # Tier 4 top
            (18, 2, 12),
            (19, 1, 14),
            (20, 0, 16), # Tier 4 bottom
            (21, 2, 12), # Lower bough fringe
        ]

    inside = set()
    for gy, gx0, gw in tiers:
        for gx in range(gx0, gx0 + gw):
            inside.add((gx, gy))

    for (gx, gy) in inside:
        is_border = any((gx+dx, gy+dy) not in inside for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])
        if is_border:
            draw_scaled_pixel(img, x0, y0, gx, gy, OUTLINE)
        else:
            # 3/4 RPG Maker shading: top-left brighter, bottom/edges darker
            if gy in (8, 12, 16, 20):
                draw_scaled_pixel(img, x0, y0, gx, gy, PINE_DARK)
            elif gx <= 7 and gy % 2 == 1:
                draw_scaled_pixel(img, x0, y0, gx, gy, PINE_LIGHT)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, PINE_MID)

    # Snow frosting on branch tips for variant 3
    if variant == 3:
        for gy, gx0, gw in [(8,5,6), (12,3,10), (16,2,12), (20,1,14)]:
            for gx in range(gx0+1, gx0+gw-1, 2):
                draw_scaled_pixel(img, x0, y0, gx, gy-1, PINE_SNOW)

    # Diagonal Gold Tinsel Garland strands across the tree
    garland_pts = [
        (6, 7), (7, 8), (8, 8), (9, 9),
        (5, 11), (6, 11), (7, 12), (8, 12), (9, 13), (10, 13),
        (4, 15), (5, 15), (6, 16), (7, 16), (8, 17), (9, 17), (10, 18), (11, 18),
    ]
    for gx, gy in garland_pts:
        if (gx, gy) in inside:
            draw_scaled_pixel(img, x0, y0, gx, gy, GARLAND)

    # Colorful Ornaments (Red, Blue, Gold, Pink) & Twinkling Fairy Lights
    ornaments = [
        (7, 6, LIGHT_GLOW),
        (6, 8, ORN_RED), (9, 7, ORN_BLUE),
        (5, 10, ORN_GOLD), (8, 10, ORN_RED), (10, 11, LIGHT_GLOW),
        (4, 14, ORN_BLUE), (7, 14, LIGHT_GLOW), (10, 14, ORN_RED), (11, 15, ORN_GOLD),
        (3, 18, ORN_RED), (6, 18, ORN_BLUE), (9, 19, LIGHT_GLOW), (12, 18, ORN_PINK),
        (5, 20, LIGHT_GLOW), (8, 20, ORN_RED), (11, 20, ORN_BLUE),
    ]
    for gx, gy, col in ornaments:
        if (gx, gy) in inside:
            draw_scaled_pixel(img, x0, y0, gx, gy, col)

    # Golden Star Topper at the very peak (gy=2..5, gx=6..9)
    draw_rect_2x(img, x0, y0, 6, 2, 4, 4, OUTLINE)
    draw_scaled_pixel(img, x0, y0, 7, 2, STAR_GOLD)
    draw_scaled_pixel(img, x0, y0, 8, 2, STAR_GOLD)
    draw_rect_2x(img, x0, y0, 6, 3, 4, 2, STAR_GOLD)
    draw_scaled_pixel(img, x0, y0, 8, 4, STAR_SHADE)
    draw_scaled_pixel(img, x0, y0, 7, 3, LIGHT_GLOW)

    # Variant 1: Add Wrapped Holiday Presents around the base of the pot!
    if variant == 1:
        # Left blue gift box with gold ribbon (gx=1..5, gy=26..31)
        draw_box_2x(img, x0, y0, 1, 26, 5, 5, ORN_BLUE, OUTLINE)
        draw_rect_2x(img, x0, y0, 3, 27, 1, 3, POT_GOLD)
        draw_rect_2x(img, x0, y0, 2, 28, 3, 1, POT_GOLD)
        # Right gold/red gift box (gx=10..14, gy=25..31)
        draw_box_2x(img, x0, y0, 10, 25, 5, 6, POT_GOLD, OUTLINE)
        draw_rect_2x(img, x0, y0, 12, 26, 1, 4, ORN_RED)
        draw_rect_2x(img, x0, y0, 11, 27, 3, 1, ORN_RED)

for v in range(4):
    make_christmas_tree(sheet, v*32, 14*32, variant=v)

# Also save standalone Christmas tree PNG in ha_floorplan/
sheet.crop((2*32, 14*32, 3*32, 16*32)).save('www/christmas_tree.png')

# ==============================================================================
# 8. POKEMON CENTER PIKACHU POWER GENERATOR (Viridian City Ep. 2 Crystal Cage!)
#    - Rows 14..15, Cols 4..5: 2x2 (64x64 px) Full Generator Station + Crystal Cage
#    - Rows 14..15, Col 6:     1x2 (32x64 px) Empty Crystal Containment Tube
#    - Rows 14..15, Col 7:     1x2 (32x64 px) Crystal Containment Tube WITH Pikachu & Sparks
# ==============================================================================
MET_LIGHT  = (216, 224, 236, 255)
MET_MID    = (168, 176, 192, 255)
MET_DARK   = (112, 120, 136, 255)
MET_PANEL  = (56, 64, 80, 255)
GLASS_FILL = (120, 224, 248, 95)   # Semi-transparent crystal cyan!
GLASS_EDGE = (72, 176, 216, 220)   # Glowing crystal rim
GLASS_HI   = (224, 252, 255, 190)  # Specular reflection streak on crystal cylinder
COIL_COPPER= (216, 128, 56, 255)
COIL_GOLD  = (248, 208, 64, 255)
HAZ_YELLOW = (248, 208, 48, 255)
HAZ_BLACK  = (48, 48, 56, 255)
LED_GREEN  = (72, 232, 112, 255)
LED_RED    = (248, 72, 72, 255)

# Pikachu Palette
PIKA_YEL   = (255, 224, 48, 255)
PIKA_SHADE = (224, 176, 24, 255)
PIKA_EAR   = (40, 40, 48, 255)
PIKA_CHEEK = (248, 64, 56, 255)
PIKA_EYE   = (32, 32, 40, 255)
SPARK_YEL  = (255, 248, 88, 255)
SPARK_WHT  = (255, 255, 240, 255)
SPARK_GLOW = (255, 216, 40, 160)

def draw_pikachu_sprite(img, x0, y0, gx_off=0, gy_off=0, pose='idle', direction='S'):
    """Draw a super crisp 2x GBA-scale Pikachu centered inside a 32x32 region (gx=0..15, gy=0..15)."""
    by = gy_off + (-1 if pose == 'jump' else 0)
    # Shadow
    draw_rect_2x(img, x0, y0, gx_off+4, gy_off+13, 8, 2, SHADOW)

    if direction == 'N':
        # Back view of Pikachu with brown back stripes
        draw_box_2x(img, x0, y0, gx_off+4, by+7, 8, 6, PIKA_YEL, OUTLINE)
        draw_rect_2x(img, x0, y0, gx_off+6, by+8, 4, 1, TRUNK_DARK)
        draw_rect_2x(img, x0, y0, gx_off+6, by+10, 4, 1, TRUNK_DARK)
        draw_box_2x(img, x0, y0, gx_off+4, by+2, 8, 6, PIKA_YEL, OUTLINE)
        # Ears
        draw_box_2x(img, x0, y0, gx_off+3, by+0, 3, 3, PIKA_YEL, OUTLINE)
        draw_scaled_pixel(img, x0, y0, gx_off+4, by+0, PIKA_EAR)
        draw_box_2x(img, x0, y0, gx_off+10, by+0, 3, 3, PIKA_YEL, OUTLINE)
        draw_scaled_pixel(img, x0, y0, gx_off+11, by+0, PIKA_EAR)
        # Lightning tail on right
        draw_rect_2x(img, x0, y0, gx_off+11, by+6, 3, 4, OUTLINE)
        draw_scaled_pixel(img, x0, y0, gx_off+12, by+7, PIKA_YEL)
        draw_scaled_pixel(img, x0, y0, gx_off+13, by+6, PIKA_YEL)
        return

    # Lightning-bolt Tail sticking out on right (gx=11..14, gy=5..10)
    draw_rect_2x(img, x0, y0, gx_off+11, by+8, 2, 2, PIKA_SHADE)
    draw_rect_2x(img, x0, y0, gx_off+12, by+6, 3, 3, OUTLINE)
    draw_scaled_pixel(img, x0, y0, gx_off+13, by+7, PIKA_YEL)
    draw_scaled_pixel(img, x0, y0, gx_off+13, by+6, PIKA_YEL)
    draw_scaled_pixel(img, x0, y0, gx_off+14, by+5, PIKA_YEL)

    # Body (gx=4..11, gy=7..13)
    draw_box_2x(img, x0, y0, gx_off+4, by+7, 8, 6, PIKA_YEL, OUTLINE)
    draw_rect_2x(img, x0, y0, gx_off+5, by+11, 6, 1, PIKA_SHADE)
    # Little yellow feet
    draw_scaled_pixel(img, x0, y0, gx_off+5, by+13, PIKA_SHADE)
    draw_scaled_pixel(img, x0, y0, gx_off+10, by+13, PIKA_SHADE)

    # Head (gx=4..11, gy=2..8)
    draw_box_2x(img, x0, y0, gx_off+4, by+2, 8, 6, PIKA_YEL, OUTLINE)
    # Left & Right Pointed Ears with black tips!
    draw_box_2x(img, x0, y0, gx_off+3, by+0, 3, 3, PIKA_YEL, OUTLINE)
    draw_scaled_pixel(img, x0, y0, gx_off+3, by+0, PIKA_EAR)
    draw_scaled_pixel(img, x0, y0, gx_off+4, by+0, PIKA_EAR)
    draw_box_2x(img, x0, y0, gx_off+10, by+0, 3, 3, PIKA_YEL, OUTLINE)
    draw_scaled_pixel(img, x0, y0, gx_off+11, by+0, PIKA_EAR)
    draw_scaled_pixel(img, x0, y0, gx_off+12, by+0, PIKA_EAR)

    # Eyes
    draw_scaled_pixel(img, x0, y0, gx_off+6, by+4, PIKA_EYE)
    draw_scaled_pixel(img, x0, y0, gx_off+9, by+4, PIKA_EYE)
    # Red Electric Cheeks!
    cheek_col = SPARK_WHT if pose == 'thunder' else PIKA_CHEEK
    draw_scaled_pixel(img, x0, y0, gx_off+5, by+6, cheek_col)
    draw_scaled_pixel(img, x0, y0, gx_off+10, by+6, cheek_col)
    # Cute nose/mouth
    draw_scaled_pixel(img, x0, y0, gx_off+7, by+5, OUTLINE)
    if pose in ('jump', 'thunder'):
        draw_scaled_pixel(img, x0, y0, gx_off+8, by+6, ORN_RED) # open mouth!

# 8A. 1x2 Crystal Containment Cage (Col 6 = Empty Cage, Col 7 = Cage with Pikachu + Sparks)
def make_crystal_cage_1x2(img, x0, y0, with_pikachu=False):
    # Floor shadow
    draw_rect_2x(img, x0, y0, 1, 29, 14, 2, SHADOW)

    # Heavy Metallic Generator Base Platform (gy=22..30, gx=1..14)
    draw_box_2x(img, x0, y0, 1, 22, 14, 8, MET_MID, OUTLINE)
    draw_box_2x(img, x0, y0, 2, 22, 12, 3, MET_LIGHT, OUTLINE)
    # Hazard stripes on front of generator base (gy=26..27)
    for gx in range(3, 13):
        col = HAZ_YELLOW if gx % 2 == 0 else HAZ_BLACK
        draw_scaled_pixel(img, x0, y0, gx, 26, col)
        draw_scaled_pixel(img, x0, y0, gx, 27, col)
    # Glowing conductive copper pad inside base (gy=22..23, gx=4..11)
    draw_rect_2x(img, x0, y0, 4, 22, 8, 2, COIL_COPPER)
    draw_rect_2x(img, x0, y0, 5, 22, 6, 1, COIL_GOLD)

    # Back edge of Crystal Cylinder (gy=6..22, gx=2..13)
    draw_rect_2x(img, x0, y0, 2, 6, 12, 16, GLASS_FILL)
    for gy in range(6, 23):
        draw_scaled_pixel(img, x0, y0, 2, gy, GLASS_EDGE)
        draw_scaled_pixel(img, x0, y0, 13, gy, GLASS_EDGE)

    # Optional Pikachu + Lightning inside the chamber!
    if with_pikachu:
        draw_pikachu_sprite(img, x0, y0, gx_off=0, gy_off=9, pose='thunder')
        # Lightning bolts inside crystal tube
        sparks = [(3, 9), (4, 8), (12, 9), (11, 8), (4, 15), (12, 16), (7, 7), (8, 6)]
        for sx, sy in sparks:
            draw_scaled_pixel(img, x0, y0, sx, sy, SPARK_YEL)
        draw_scaled_pixel(img, x0, y0, 4, 9, SPARK_WHT)
        draw_scaled_pixel(img, x0, y0, 11, 9, SPARK_WHT)

    # Front Specular Glass Reflection Streaks (drawn OVER Pikachu so he looks trapped inside the crystal!)
    for gy in range(7, 21):
        draw_scaled_pixel(img, x0, y0, 4, gy, GLASS_HI)
        if gy % 3 != 0:
            draw_scaled_pixel(img, x0, y0, 11, gy, GLASS_HI)
    # Bottom crystal rim curve
    draw_rect_2x(img, x0, y0, 3, 21, 10, 1, GLASS_EDGE)

    # Top Metallic High-Voltage Collector Cap & Tesla Coil (gy=1..7, gx=1..14)
    draw_box_2x(img, x0, y0, 1, 3, 14, 4, MET_MID, OUTLINE)
    draw_rect_2x(img, x0, y0, 2, 4, 12, 1, MET_LIGHT)
    # Power status LEDs on top rim
    draw_scaled_pixel(img, x0, y0, 4, 5, LED_GREEN)
    draw_scaled_pixel(img, x0, y0, 6, 5, COIL_GOLD)
    draw_scaled_pixel(img, x0, y0, 11, 5, LED_RED)
    # Top copper collector coil dome (gy=0..3, gx=5..10)
    draw_box_2x(img, x0, y0, 5, 0, 6, 4, COIL_COPPER, OUTLINE)
    draw_rect_2x(img, x0, y0, 6, 1, 4, 1, COIL_GOLD)

make_crystal_cage_1x2(sheet, 6*32, 14*32, with_pikachu=False)
make_crystal_cage_1x2(sheet, 7*32, 14*32, with_pikachu=True)

# 8B. 2x2 Full Pokémon Center Power Generator Station (Cols 4..5, Rows 14..15 -> 64x64 px)
#     Left & Right sides have high-voltage Tesla coils, power cables, and energy meters;
#     Center has a wide Crystal Containment Dome!
def make_generator_station_2x2(img, x0, y0):
    # Full 32x32 2x-grid (64x64 px)
    # Floor shadow across both tiles
    draw_rect_2x(img, x0, y0, 2, 29, 28, 2, SHADOW)

    # Heavy Base Platform across gx=2..29, gy=21..29
    draw_box_2x(img, x0, y0, 2, 21, 28, 9, MET_MID, OUTLINE)
    draw_box_2x(img, x0, y0, 3, 21, 26, 3, MET_LIGHT, OUTLINE)
    # Hazard stripe band across bottom front (gy=26..27)
    for gx in range(4, 28):
        col = HAZ_YELLOW if gx % 2 == 0 else HAZ_BLACK
        draw_scaled_pixel(img, x0, y0, gx, 26, col)
        draw_scaled_pixel(img, x0, y0, gx, 27, col)

    # Left & Right High-Voltage Tesla Coils / Capacitor Towers (gx=2..7 and gx=24..29, gy=6..22)
    for tx in (2, 24):
        draw_box_2x(img, x0, y0, tx, 6, 6, 16, MET_DARK, OUTLINE)
        # Copper coil rings
        for cy in (8, 11, 14, 17):
            draw_box_2x(img, x0, y0, tx, cy, 6, 2, COIL_COPPER, OUTLINE)
            draw_rect_2x(img, x0, y0, tx+1, cy, 4, 1, COIL_GOLD)
        # Top ceramic insulator sphere
        draw_box_2x(img, x0, y0, tx+1, 3, 4, 4, GLASS_HI, OUTLINE)
        draw_rect_2x(img, x0, y0, tx+2, 4, 2, 2, COIL_GOLD)

    # Center Conductive Pad (gx=9..22, gy=21..23)
    draw_box_2x(img, x0, y0, 9, 21, 14, 3, COIL_COPPER, OUTLINE)
    draw_rect_2x(img, x0, y0, 11, 22, 10, 1, COIL_GOLD)

    # Center Crystal Containment Chamber (gx=8..23, gy=5..21)
    draw_rect_2x(img, x0, y0, 8, 5, 16, 16, GLASS_FILL)
    for gy in range(5, 22):
        draw_scaled_pixel(img, x0, y0, 8, gy, GLASS_EDGE)
        draw_scaled_pixel(img, x0, y0, 23, gy, GLASS_EDGE)
    # Specular reflection bars on crystal dome
    for gy in range(6, 20):
        draw_scaled_pixel(img, x0, y0, 10, gy, GLASS_HI)
        if gy % 2 == 0:
            draw_scaled_pixel(img, x0, y0, 11, gy, GLASS_HI)
        draw_scaled_pixel(img, x0, y0, 21, gy, GLASS_HI)
    draw_rect_2x(img, x0, y0, 9, 20, 14, 1, GLASS_EDGE)

    # Upper Bridge Canopy & Energy Meter (gx=6..25, gy=1..6)
    draw_box_2x(img, x0, y0, 6, 1, 20, 5, MET_MID, OUTLINE)
    draw_rect_2x(img, x0, y0, 7, 2, 18, 1, MET_LIGHT)
    # Center Voltage Monitor Screen (gx=12..19, gy=2..5)
    draw_box_2x(img, x0, y0, 12, 2, 8, 3, MET_PANEL, OUTLINE)
    draw_scaled_pixel(img, x0, y0, 13, 3, LED_GREEN)
    draw_scaled_pixel(img, x0, y0, 14, 3, LED_GREEN)
    draw_scaled_pixel(img, x0, y0, 15, 3, HAZ_YELLOW)
    draw_scaled_pixel(img, x0, y0, 16, 3, HAZ_YELLOW)
    draw_scaled_pixel(img, x0, y0, 17, 3, LED_RED)
    draw_scaled_pixel(img, x0, y0, 18, 3, SPARK_WHT)

make_generator_station_2x2(sheet, 4*32, 14*32)

# 8C. Row 16 (y=512..544):
#     Cols 0..3: Standalone Pikachu sprites (S, N, Idle-Spark, Thunder-Jump)
#     Cols 4..5: Left & Right Power Generator Coils (1x1 modular tiles)
#     Cols 6..7: Standalone Crystal Glass Dome Overlay (1x2 or 1x1)
draw_pikachu_sprite(sheet, 0*32, 16*32, pose='idle', direction='S')
draw_pikachu_sprite(sheet, 1*32, 16*32, pose='idle', direction='N')
draw_pikachu_sprite(sheet, 2*32, 16*32, pose='jump', direction='S')
draw_pikachu_sprite(sheet, 3*32, 16*32, pose='thunder', direction='S')
# Add sparks around Col 3 Pikachu
for sx, sy in [(2, 3), (3, 2), (13, 3), (12, 2), (2, 10), (13, 11)]:
    draw_scaled_pixel(sheet, 3*32, 16*32, sx, sy, SPARK_YEL)

# Save updated custom_home_items.png
sheet.save('tilesets/custom_home_items.png')

# Update custom_home_items.tsx to reflect 17 rows (136 tiles, height 544)
tsx_content = """<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="custom_home_items" tilewidth="32" tileheight="32" tilecount="136" columns="8">
 <image source="custom_home_items.png" width="256" height="544"/>
</tileset>
"""
with open('tilesets/custom_home_items.tsx', 'w') as f:
    f.write(tsx_content)

# ==============================================================================
# 9. GENERATE ANIMATED PIKACHU LIGHTNING GIFS FOR HOME ASSISTANT!
#    - www/pikachu_thunder.gif (64x64 px)
#    - www/pikachu_idle.gif    (64x64 px)
# ==============================================================================
# Why 64x64 px (32x32 in 2x GBA pixels)?
# Because lightning bolts shoot OUTWARD from Pikachu's cheeks & tail across the crystal cage
# and to the side coils! Centered at (16, 16) in 2x-grid (32, 32 in pixels).

def make_thunder_gif():
    frames = []
    # 6-frame high-energy Pokémon Center electric generator animation!
    # Frame 0: Pikachu crouching, cheeks glowing red/yellow
    # Frame 1: Pikachu charging, small yellow sparks around cheeks & tail
    # Frame 2: Pikachu leaps up! Bright yellow lightning arcs shoot left & right!
    # Frame 3: Maximum Thunderbolt! White-hot & yellow branching lightning bolts + electric aura ring!
    # Frame 4: Secondary lightning arc discharge to top & sides!
    # Frame 5: Landing with residual electric sparks crackling!
    for f_idx in range(6):
        frm = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        pose = 'idle' if f_idx in (0, 1, 5) else ('jump' if f_idx == 2 else 'thunder')
        gy_off = 9 if f_idx in (0, 1, 5) else 8

        # In frames 2, 3, 4, add an electric golden aura glow behind Pikachu!
        if f_idx in (2, 3, 4):
            aura_col = (255, 240, 64, 90) if f_idx != 3 else (255, 255, 160, 130)
            draw_rect_2x(frm, 0, 0, 9, 9, 14, 13, aura_col)

        # Draw Pikachu centered at gx_off=8, gy_off=8 (center of 32x32 2x-grid = 64x64 px)
        draw_pikachu_sprite(frm, 0, 0, gx_off=8, gy_off=gy_off, pose=pose, direction='S')

        # Frame-specific lightning bolts & sparks!
        if f_idx == 1:
            # Cheek sparks charging up
            for gx, gy in [(11, 14), (12, 13), (20, 14), (19, 13), (22, 12)]:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_YEL)
        elif f_idx == 2:
            # Medium lightning arcs shooting out left, right, and up!
            bolts = [
                # Left arc
                (11, 13), (10, 12), (9, 13), (8, 11), (7, 12), (6, 10), (5, 11),
                # Right arc
                (20, 13), (21, 12), (22, 13), (23, 11), (24, 12), (25, 10), (26, 11),
                # Top arc
                (15, 7), (16, 6), (15, 5), (17, 4), (16, 3),
            ]
            for gx, gy in bolts:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_YEL)
            for gx, gy in [(11, 13), (20, 13), (16, 6), (8, 11), (23, 11)]:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_WHT)
        elif f_idx == 3:
            # FULL THUNDERBOLT DISCHARGE! Branching yellow + white-core lightning bolts to all 4 corners & coils!
            bolts_yel = [
                # Left coil bolt
                (11, 13), (10, 13), (9, 11), (8, 12), (7, 10), (6, 10), (5, 8), (4, 9), (3, 7),
                (7, 13), (6, 14), (5, 16), (4, 15),
                # Right coil bolt
                (20, 13), (21, 13), (22, 11), (23, 12), (24, 10), (25, 10), (26, 8), (27, 9), (28, 7),
                (24, 13), (25, 14), (26, 16), (27, 15),
                # Upper collector dome bolt
                (14, 7), (13, 5), (14, 4), (13, 2), (15, 1),
                (17, 7), (18, 5), (17, 4), (18, 2), (16, 1),
                # Lower pad sparks
                (10, 19), (9, 20), (21, 19), (22, 20),
            ]
            for gx, gy in bolts_yel:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_YEL)
            bolts_wht = [
                (11, 13), (9, 11), (7, 10), (5, 8),
                (20, 13), (22, 11), (24, 10), (26, 8),
                (14, 7), (14, 4), (17, 7), (17, 4),
            ]
            for gx, gy in bolts_wht:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_WHT)
        elif f_idx == 4:
            # Outer electric ring & crackling zig-zags
            bolts = [
                (10, 14), (8, 15), (6, 13), (4, 14), (3, 12),
                (21, 14), (23, 15), (25, 13), (27, 14), (28, 12),
                (12, 6), (11, 4), (10, 3),
                (19, 6), (20, 4), (21, 3),
                (7, 18), (6, 19), (24, 18), (25, 19),
            ]
            for gx, gy in bolts:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_YEL)
            for gx, gy in [(8, 15), (23, 15), (11, 4), (20, 4)]:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_WHT)
        elif f_idx == 5:
            # Residual sparks around cage
            for gx, gy in [(9, 10), (22, 10), (7, 16), (24, 16), (15, 5)]:
                draw_scaled_pixel(frm, 0, 0, gx, gy, SPARK_YEL)

        # Overlay subtle front glass reflection streaks so Pikachu still looks inside the crystal cylinder!
        for gy in range(6, 20):
            draw_scaled_pixel(frm, 0, 0, 10, gy, (224, 252, 255, 90))
        frames.append(frm)

    # Save transparent animated GIF using PIL palette with disposal=2 (restore to background between frames!)
    pal_frames = []
    for f in frames:
        alpha = f.getchannel('A')
        p_frm = f.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 64 else 0)
        p_frm.paste(255, mask)
        p_frm.info['transparency'] = 255
        pal_frames.append(p_frm)

    out_path = 'www/pikachu_thunder.gif'
    pal_frames[0].save(
        out_path,
        save_all=True,
        append_images=pal_frames[1:],
        duration=[180, 140, 110, 130, 110, 180],
        loop=0,
        disposal=2,
        transparency=255
    )

    # Also save a calmer pikachu_idle.gif (frames 0, 1, 5)
    idle_frames = [pal_frames[0], pal_frames[1], pal_frames[5]]
    idle_frames[0].save(
        'www/pikachu_idle.gif',
        save_all=True,
        append_images=idle_frames[1:],
        duration=[350, 220, 350],
        loop=0,
        disposal=2,
        transparency=255
    )

make_thunder_gif()
print("Successfully generated Christmas Trees, Crystal Generator Cages, and Pikachu GIFs!")
from PIL import Image

sheet = Image.open('tilesets/custom_home_items.png').convert('RGBA')
# Expand from 17 rows (544 px) to 18 rows (576 px) so we have Row 16 Cols 4..7 AND Row 17 Cols 0..7!
W, H = 256, 576
new_sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
new_sheet.paste(sheet, (0, 0))

def draw_scaled_pixel(img, x0, y0, gx, gy, color):
    if color is None:
        return
    px = img.load()
    for dy in range(2):
        for dx in range(2):
            ix, iy = x0 + gx*2 + dx, y0 + gy*2 + dy
            if 0 <= ix < img.width and 0 <= iy < img.height:
                px[ix, iy] = color

def draw_rect_2x(img, x0, y0, gx0, gy0, gw, gh, color):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            draw_scaled_pixel(img, x0, y0, gx, gy, color)

def draw_box_2x(img, x0, y0, gx0, gy0, gw, gh, fill, outline):
    for gy in range(gy0, gy0 + gh):
        for gx in range(gx0, gx0 + gw):
            if gx == gx0 or gx == gx0 + gw - 1 or gy == gy0 or gy == gy0 + gh - 1:
                draw_scaled_pixel(img, x0, y0, gx, gy, outline)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, fill)

OUTLINE   = (40, 44, 56, 255)
SHADOW    = (0, 0, 0, 60)
PS_WHITE  = (246, 248, 252, 255)
PS_SHADE  = (210, 218, 230, 255)
PS_BLACK  = (28, 32, 42, 255)
PS_GLOSS  = (60, 68, 84, 255)
PS_LED_B  = (56, 152, 255, 255)   # Iconic PS5 Blue LED glow!
PS_LED_HI = (160, 224, 255, 255)  # Bright cyan-white LED core
PS_STAND  = (52, 56, 68, 255)

def make_ps5_vertical(img, x0, y0, direction='S', with_controller=True):
    """
    1x1 (32x32 px) Vertical PlayStation 5 Console in 2x GBA pixel art!
    - Iconic tall white flared side panels + glossy black center core + glowing blue LED strip
    - Optional DualSense controller next to it!
    """
    cx = 2 if with_controller else 4  # shift slightly left if controller is on the right
    # Floor / desk shadow
    draw_rect_2x(img, x0, y0, cx, 13, 8, 2, SHADOW)
    # Circular black base stand (gy=13)
    draw_rect_2x(img, x0, y0, cx+1, 13, 6, 1, PS_STAND)

    if direction == 'S':
        # Facing South (Front of PS5: narrow profile showing both curved white wing plates, black center column, and glowing blue LEDs!)
        # Outer outline box (gx=cx+1..cx+6, gy=1..13)
        draw_box_2x(img, x0, y0, cx+1, 1, 6, 12, PS_WHITE, OUTLINE)
        # Flared top corners of PS5 white plates (popped Collar look at gy=1..2)
        draw_scaled_pixel(img, x0, y0, cx+1, 1, OUTLINE)
        draw_scaled_pixel(img, x0, y0, cx+6, 1, OUTLINE)
        draw_scaled_pixel(img, x0, y0, cx+2, 2, PS_WHITE)
        draw_scaled_pixel(img, x0, y0, cx+5, 2, PS_WHITE)
        # Glossy black center core running down the middle (gx=cx+3..cx+4, gy=2..12)
        draw_rect_2x(img, x0, y0, cx+3, 2, 2, 10, PS_BLACK)
        draw_scaled_pixel(img, x0, y0, cx+3, 4, PS_GLOSS)
        # Glowing Blue PS5 LED strips flanking the black core at the top!
        draw_scaled_pixel(img, x0, y0, cx+3, 2, PS_LED_HI)
        draw_scaled_pixel(img, x0, y0, cx+4, 2, PS_LED_HI)
        draw_scaled_pixel(img, x0, y0, cx+3, 3, PS_LED_B)
        draw_scaled_pixel(img, x0, y0, cx+4, 3, PS_LED_B)
        draw_scaled_pixel(img, x0, y0, cx+3, 5, PS_LED_B)
        draw_scaled_pixel(img, x0, y0, cx+4, 5, PS_LED_B)
        # Left & right white side plates inner highlight/shade
        for gy in range(2, 12):
            draw_scaled_pixel(img, x0, y0, cx+2, gy, PS_WHITE)
            draw_scaled_pixel(img, x0, y0, cx+5, gy, PS_SHADE)

    elif direction == 'N':
        # Facing North (Back of PS5: exhaust vents in center black column, white wing plates on sides)
        draw_box_2x(img, x0, y0, cx+1, 1, 6, 12, PS_SHADE, OUTLINE)
        draw_rect_2x(img, x0, y0, cx+3, 2, 2, 10, PS_BLACK)
        for gy in range(3, 11, 2):
            draw_scaled_pixel(img, x0, y0, cx+3, gy, PS_GLOSS)

    elif direction in ('E', 'W'):
        # Side / 3/4 Profile (shows the full curved white faceplate of the PS5 + black front strip with blue LED on East or West edge!)
        px0 = cx if with_controller else 3
        draw_rect_2x(img, x0, y0, px0, 13, 9, 2, SHADOW)
        draw_rect_2x(img, x0, y0, px0+2, 13, 5, 1, PS_STAND)
        # Wide white side plate (gx=px0+1..px0+7, gy=1..13)
        draw_box_2x(img, x0, y0, px0+1, 1, 7, 12, PS_WHITE, OUTLINE)
        # Subtle 3/4 shading along bottom & back of white faceplate
        draw_rect_2x(img, x0, y0, px0+2, 11, 5, 1, PS_SHADE)
        if direction == 'E':
            # Front black edge & blue LED on the RIGHT (East) side (gx=px0+6)
            draw_rect_2x(img, x0, y0, px0+6, 2, 1, 10, PS_BLACK)
            draw_scaled_pixel(img, x0, y0, px0+6, 2, PS_LED_HI)
            draw_scaled_pixel(img, x0, y0, px0+6, 3, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, px0+6, 4, PS_LED_B)
            # Tiny PS logo hint on upper-left of white plate
            draw_scaled_pixel(img, x0, y0, px0+3, 3, PS_SHADE)
        else:
            # Front black edge & blue LED on the LEFT (West) side (gx=px0+2)
            draw_rect_2x(img, x0, y0, px0+2, 2, 1, 10, PS_BLACK)
            draw_scaled_pixel(img, x0, y0, px0+2, 2, PS_LED_HI)
            draw_scaled_pixel(img, x0, y0, px0+2, 3, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, px0+2, 4, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, px0+5, 3, PS_SHADE)

    # Optional DualSense Controller sitting next to the PS5 (gx=10..14, gy=9..13)
    if with_controller:
        draw_rect_2x(img, x0, y0, 10, 13, 5, 1, SHADOW)
        draw_box_2x(img, x0, y0, 10, 9, 5, 4, PS_WHITE, OUTLINE)
        # Black lower grips / thumbsticks in center of DualSense
        draw_rect_2x(img, x0, y0, 11, 11, 3, 1, PS_BLACK)
        # Blue lightbar accent around touchpad
        draw_scaled_pixel(img, x0, y0, 12, 10, PS_LED_B)

def make_ps5_horizontal(img, x0, y0, direction='S'):
    """
    1x1 (32x32 px) Horizontal PlayStation 5 Console (lying flat on TV stand/shelf) + DualSense!
    """
    draw_rect_2x(img, x0, y0, 1, 12, 14, 2, SHADOW)
    if direction in ('S', 'N'):
        # Horizontal console body (gx=1..14, gy=6..12)
        draw_box_2x(img, x0, y0, 1, 6, 14, 6, PS_WHITE, OUTLINE)
        # Top white plate surface (gy=7..8)
        draw_rect_2x(img, x0, y0, 2, 7, 12, 2, PS_WHITE)
        draw_rect_2x(img, x0, y0, 2, 9, 12, 1, PS_SHADE)
        if direction == 'S':
            # Front glossy black strip + glowing blue LED strip across the front!
            draw_rect_2x(img, x0, y0, 2, 10, 12, 1, PS_BLACK)
            draw_scaled_pixel(img, x0, y0, 3, 10, PS_LED_HI)
            draw_scaled_pixel(img, x0, y0, 4, 10, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, 5, 10, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, 10, 10, PS_LED_B)
            draw_scaled_pixel(img, x0, y0, 11, 10, PS_LED_HI)
        else:
            draw_rect_2x(img, x0, y0, 3, 10, 10, 1, PS_GLOSS)
    else:
        # Horizontal oriented North-South (gx=4..11, gy=2..13)
        draw_box_2x(img, x0, y0, 4, 2, 8, 11, PS_WHITE, OUTLINE)
        sx = 10 if direction == 'E' else 5
        draw_rect_2x(img, x0, y0, sx, 3, 1, 9, PS_BLACK)
        draw_scaled_pixel(img, x0, y0, sx, 4, PS_LED_HI)
        draw_scaled_pixel(img, x0, y0, sx, 5, PS_LED_B)
        draw_scaled_pixel(img, x0, y0, sx, 9, PS_LED_B)

# Place in Row 16, Cols 4..7: Vertical PS5 + DualSense Controller (S, N, E, W)
for idx, d in enumerate(['S', 'N', 'E', 'W']):
    make_ps5_vertical(new_sheet, (idx+4)*32, 16*32, direction=d, with_controller=True)
    # Row 17, Cols 0..3: Compact Vertical PS5 Only (no controller, great for tight desks!) (S, N, E, W)
    make_ps5_vertical(new_sheet, idx*32, 17*32, direction=d, with_controller=False)
    # Row 17, Cols 4..7: Horizontal PS5 (S, N, E, W)
    make_ps5_horizontal(new_sheet, (idx+4)*32, 17*32, direction=d)

new_sheet.save('tilesets/custom_home_items.png')

tsx_content = """<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="custom_home_items" tilewidth="32" tileheight="32" tilecount="144" columns="8">
 <image source="custom_home_items.png" width="256" height="576"/>
</tileset>
"""
with open('tilesets/custom_home_items.tsx', 'w') as f:
    f.write(tsx_content)

# Save a zoomed preview of Rows 14..17
crop = new_sheet.crop((0, 14*32, 256, 18*32))
bg = Image.new("RGBA", (crop.width*3, crop.height*3), (210, 216, 226, 255))
bg.alpha_composite(crop.resize((crop.width*3, crop.height*3), Image.NEAREST))
bg.save("/tmp/preview_ps5_tiles.png")
print("Added PS5 1x1 tiles to custom_home_items.png!")
from PIL import Image
import math

old_sheet = Image.open('tilesets/custom_home_items.png').convert('RGBA')
# Old sheet is 256 x 576 (8 cols x 18 rows, rows 0..17).
# We add 4 bands of 3 rows = 12 rows (rows 18..29) -> Total 30 rows = 256 x 960 px!
W, H = 256, 960
sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sheet.paste(old_sheet.crop((0, 0, 256, 576)), (0, 0))

def draw_scaled_pixel(img, x0, y0, gx, gy, color):
    """Draw a 2x2 pixel block (authentic 2x GBA pixel scale) inside a 128x96 (64x48 2x-grid) canvas."""
    if color is None:
        return
    px = img.load()
    for dy in range(2):
        for dx in range(2):
            ix, iy = x0 + gx*2 + dx, y0 + gy*2 + dy
            if 0 <= ix < img.width and 0 <= iy < img.height:
                px[ix, iy] = color

def draw_circle_2x(img, x0, y0, cx, cy, r, fill, outline=None):
    for gy in range(int(cy - r - 2), int(cy + r + 3)):
        for gx in range(int(cx - r - 2), int(cx + r + 3)):
            dist = math.hypot(gx - cx, gy - cy)
            if dist <= r:
                draw_scaled_pixel(img, x0, y0, gx, gy, fill)

OUTLINE     = (44, 52, 68, 255)

# Cloud Palettes (Light Fluffy vs Dark Storm)
CLD_LIGHT_HI  = (252, 254, 255, 255)
CLD_LIGHT_MID = (232, 240, 250, 255)
CLD_LIGHT_SHD = (188, 204, 224, 255)

CLD_GREY_HI   = (216, 224, 236, 255)
CLD_GREY_MID  = (176, 188, 208, 255)
CLD_GREY_SHD  = (136, 148, 172, 255)

CLD_STORM_HI  = (144, 156, 180, 255)
CLD_STORM_MID = (104, 116, 140, 255)
CLD_STORM_SHD = (72, 82, 104, 255)

# Sun & Moon Palettes
SUN_CORE      = (255, 248, 144, 255)
SUN_YEL       = (255, 220, 56, 255)
SUN_ORG       = (248, 168, 32, 255)
SUN_OUTLINE   = (168, 88, 24, 255)

MOON_LIGHT    = (255, 248, 168, 255)
MOON_GOLD     = (248, 216, 72, 255)
MOON_SHADE    = (208, 168, 40, 255)

RAIN_LIGHT    = (120, 208, 255, 255)
RAIN_BLUE     = (56, 152, 232, 255)
BOLT_WHT      = (255, 255, 232, 255)
BOLT_YEL      = (255, 232, 56, 255)

def draw_fluffy_cloud(img, x0, y0, puffs, pal, outline=OUTLINE):
    """
    Draw a multi-puff RPG Maker / Pokémon style cloud with crisp 2x pixel outline and 3-tone shading!
    puffs: list of (cx, cy, r) in 2x-grid coordinates (64x48).
    Also flattens the bottom slightly at max_y for that classic pixel-art cumulus look!
    """
    hi, mid, shd = pal
    inside = set()
    max_y = max(cy + r for (_, cy, r) in puffs) - 1.5
    for gy in range(0, 48):
        for gx in range(0, 64):
            if gy > max_y:
                continue
            for (cx, cy, r) in puffs:
                if math.hypot(gx - cx, gy - cy) <= r:
                    inside.add((gx, gy))
                    break

    for (gx, gy) in inside:
        is_border = any((gx+dx, gy+dy) not in inside for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])
        if is_border:
            draw_scaled_pixel(img, x0, y0, gx, gy, outline)
        else:
            # Check distance to bottom or top of cloud for 3-tone Pokémon shading
            if (gx, gy+1) not in inside or (gx, gy+2) not in inside or (gx+1, gy+2) not in inside:
                draw_scaled_pixel(img, x0, y0, gx, gy, shd)
            elif (gx, gy-1) not in inside or (gx, gy-2) not in inside or (gx-1, gy-2) not in inside:
                draw_scaled_pixel(img, x0, y0, gx, gy, hi)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, mid)

def draw_sun(img, x0, y0, cx, cy, r=11):
    """Draw a radiant pixel-art Pokémon Sun with 8 sunbeams and warm shading."""
    # 8 Sunbeams radiating outward
    angles = [i * math.pi / 4 for i in range(8)]
    for idx, ang in enumerate(angles):
        r_start = r + 3
        r_end = r + (7 if idx % 2 == 0 else 5)
        for d in range(r_start, r_end + 1):
            gx = round(cx + d * math.cos(ang))
            gy = round(cy + d * math.sin(ang))
            # Thicken ray slightly
            draw_scaled_pixel(img, x0, y0, gx, gy, SUN_OUTLINE)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                if math.hypot((gx+dx)-cx, (gy+dy)-cy) <= r_end:
                    draw_scaled_pixel(img, x0, y0, gx+dx, gy+dy, SUN_OUTLINE)
        for d in range(r_start, r_end):
            gx = round(cx + d * math.cos(ang))
            gy = round(cy + d * math.sin(ang))
            draw_scaled_pixel(img, x0, y0, gx, gy, SUN_YEL if d < r_end-1 else SUN_ORG)

    # Sun disc
    inside = set()
    for gy in range(cy - r - 2, cy + r + 3):
        for gx in range(cx - r - 2, cx + r + 3):
            if math.hypot(gx - cx, gy - cy) <= r:
                inside.add((gx, gy))
    for (gx, gy) in inside:
        is_border = any((gx+dx, gy+dy) not in inside for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])
        if is_border:
            draw_scaled_pixel(img, x0, y0, gx, gy, SUN_OUTLINE)
        else:
            dist_tl = math.hypot(gx - (cx - 3), gy - (cy - 3))
            if dist_tl <= r * 0.45:
                draw_scaled_pixel(img, x0, y0, gx, gy, SUN_CORE)
            elif gy > cy + r * 0.45 or gx > cx + r * 0.55:
                draw_scaled_pixel(img, x0, y0, gx, gy, SUN_ORG)
            else:
                draw_scaled_pixel(img, x0, y0, gx, gy, SUN_YEL)

# ==============================================================================
# 1. SUNNY (Rows 18..20, Cols 0..3 -> x0=0, y0=18*32=576)
# ==============================================================================
draw_sun(sheet, 0, 18*32, cx=32, cy=24, r=11)
# Extra golden sun sparkles around the corners
for sx, sy in [(10, 10), (54, 12), (12, 38), (52, 36)]:
    draw_scaled_pixel(sheet, 0, 18*32, sx, sy, SUN_CORE)
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        draw_scaled_pixel(sheet, 0, 18*32, sx+dx, sy+dy, SUN_ORG)

# ==============================================================================
# 2. CLEAR-NIGHT (Rows 18..20, Cols 4..7 -> x0=128, y0=18*32=576)
# ==============================================================================
def draw_clear_night(img, x0, y0):
    cx, cy, r_out, r_cut = 32, 24, 13, 10
    inside = set()
    for gy in range(cy - r_out - 2, cy + r_out + 3):
        for gx in range(cx - r_out - 2, cx + r_out + 3):
            if math.hypot(gx - cx, gy - cy) <= r_out and math.hypot(gx - (cx + 6), gy - (cy - 4)) > r_cut:
                inside.add((gx, gy))
    for (gx, gy) in inside:
        is_border = any((gx+dx, gy+dy) not in inside for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])
        if is_border:
            draw_scaled_pixel(img, x0, y0, gx, gy, OUTLINE)
        elif gx < cx - 4 and gy < cy:
            draw_scaled_pixel(img, x0, y0, gx, gy, MOON_LIGHT)
        elif gy > cy + 5:
            draw_scaled_pixel(img, x0, y0, gx, gy, MOON_SHADE)
        else:
            draw_scaled_pixel(img, x0, y0, gx, gy, MOON_GOLD)
    # 4-point twinkling pixel stars around the crescent moon
    stars = [(12, 12, True), (50, 11, True), (46, 26, False), (15, 34, False), (52, 36, True), (24, 9, False)]
    for sx, sy, big in stars:
        draw_scaled_pixel(img, x0, y0, sx, sy, BOLT_WHT)
        if big:
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                draw_scaled_pixel(img, x0, y0, sx+dx, sy+dy, MOON_GOLD)

draw_clear_night(sheet, 128, 18*32)

# ==============================================================================
# 3. PARTLY CLOUDY (Rows 21..23, Cols 0..3 -> x0=0, y0=21*32=672)
#    Golden Sun on upper-left peeking behind a fluffy white cloud in center-right!
# ==============================================================================
draw_sun(sheet, 0, 21*32, cx=22, cy=18, r=9)
puffs_main = [(22, 31, 8), (31, 26, 11), (42, 28, 9), (50, 32, 7), (16, 33, 6)]
draw_fluffy_cloud(sheet, 0, 21*32, puffs_main, (CLD_LIGHT_HI, CLD_LIGHT_MID, CLD_LIGHT_SHD))

# ==============================================================================
# 4. CLOUDY / OVERCAST (Rows 21..23, Cols 4..7 -> x0=128, y0=21*32=672)
#    Back grey cloud + front fluffy white-grey cloud!
# ==============================================================================
puffs_back = [(18, 22, 8), (27, 17, 10), (38, 19, 8), (45, 22, 6)]
draw_fluffy_cloud(sheet, 128, 21*32, puffs_back, (CLD_GREY_HI, CLD_GREY_MID, CLD_GREY_SHD))
puffs_front = [(20, 33, 8), (31, 27, 11), (43, 29, 9), (51, 33, 7), (13, 34, 6)]
draw_fluffy_cloud(sheet, 128, 21*32, puffs_front, (CLD_LIGHT_HI, CLD_LIGHT_MID, CLD_LIGHT_SHD))

# ==============================================================================
# 5. RAINY (Rows 24..26, Cols 0..3 -> x0=0, y0=24*32=768)
#    Dark rain cloud + diagonal falling blue raindrops!
# ==============================================================================
puffs_rain = [(19, 24, 8), (30, 18, 11), (42, 20, 9), (50, 24, 7), (13, 25, 6)]
draw_fluffy_cloud(sheet, 0, 24*32, puffs_rain, (CLD_GREY_HI, CLD_GREY_MID, CLD_STORM_MID))
# Diagonal rain streaks below cloud (gy=31..44)
rain_starts = [(16, 31), (24, 32), (32, 31), (40, 32), (48, 31), (19, 38), (27, 39), (35, 38), (43, 39)]
for rx, ry in rain_starts:
    for step in range(4):
        col = RAIN_LIGHT if step == 0 else RAIN_BLUE
        draw_scaled_pixel(sheet, 0, 24*32, rx - step, ry + step, col)

# ==============================================================================
# 6. LIGHTNING / POURING STORM (Rows 24..26, Cols 4..7 -> x0=128, y0=24*32=768)
#    Dark storm cloud + heavy rain + bright yellow/white Thunderbolt lightning bolt!
# ==============================================================================
draw_fluffy_cloud(sheet, 128, 24*32, puffs_rain, (CLD_STORM_HI, CLD_STORM_MID, CLD_STORM_SHD))
for rx, ry in [(15, 31), (22, 32), (41, 31), (48, 32), (18, 38), (44, 39)]:
    for step in range(4):
        draw_scaled_pixel(sheet, 128, 24*32, rx - step, ry + step, RAIN_BLUE)
# Big jagged Thunderbolt lightning bolt shooting down from center of storm cloud (gx=28..36, gy=26..45)
bolt_pts = [
    (33, 26), (32, 27), (31, 28), (30, 29), (29, 30), (28, 31),
    (29, 31), (30, 31), (31, 31), (32, 31), (33, 31), (34, 31),
    (33, 32), (32, 33), (31, 34), (30, 35), (29, 36),
    (30, 36), (31, 36), (32, 36), (33, 36),
    (32, 37), (31, 38), (30, 39), (29, 40), (28, 41), (27, 42), (26, 43)
]
for bx, by in bolt_pts:
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        draw_scaled_pixel(sheet, 128, 24*32, bx+dx, by+dy, OUTLINE)
for bx, by in bolt_pts:
    draw_scaled_pixel(sheet, 128, 24*32, bx, by, BOLT_YEL)
    draw_scaled_pixel(sheet, 128, 24*32, bx+1, by, BOLT_WHT)

# ==============================================================================
# 7. FOG / MIST (Rows 27..29, Cols 0..3 -> x0=0, y0=27*32=864)
#    Soft cloud + layered horizontal Pokémon mist bands!
# ==============================================================================
puffs_fog = [(20, 21, 7), (31, 16, 10), (42, 18, 8), (49, 21, 6), (14, 22, 5)]
draw_fluffy_cloud(sheet, 0, 27*32, puffs_fog, (CLD_GREY_HI, CLD_GREY_MID, CLD_GREY_SHD))
# Horizontal mist bars with rounded ends below and across bottom of cloud
fog_bars = [
    (10, 29, 44),
    (14, 34, 38),
    (8,  39, 42),
    (18, 43, 30),
]
for fx, fy, fw in fog_bars:
    for gx in range(fx, fx + fw):
        draw_scaled_pixel(sheet, 0, 27*32, gx, fy-1, OUTLINE)
        draw_scaled_pixel(sheet, 0, 27*32, gx, fy, CLD_LIGHT_HI)
        draw_scaled_pixel(sheet, 0, 27*32, gx, fy+1, CLD_LIGHT_SHD)
        draw_scaled_pixel(sheet, 0, 27*32, gx, fy+2, OUTLINE)
    draw_scaled_pixel(sheet, 0, 27*32, fx-1, fy, OUTLINE)
    draw_scaled_pixel(sheet, 0, 27*32, fx-1, fy+1, OUTLINE)
    draw_scaled_pixel(sheet, 0, 27*32, fx+fw, fy, OUTLINE)
    draw_scaled_pixel(sheet, 0, 27*32, fx+fw, fy+1, OUTLINE)

# ==============================================================================
# 8. WINDY (Rows 27..29, Cols 4..7 -> x0=128, y0=27*32=864)
#    Fluffy cloud + swirling wind gust curls!
# ==============================================================================
draw_fluffy_cloud(sheet, 128, 27*32, puffs_fog, (CLD_LIGHT_HI, CLD_LIGHT_MID, CLD_LIGHT_SHD))
# Swirling wind streamlines with curled spiral tips
wind_lines = [
    [(10, 31), (28, 31), (32, 30), (34, 28), (33, 26), (31, 26)],
    [(16, 36), (44, 36), (48, 35), (50, 33), (49, 31), (47, 31)],
    [(12, 41), (36, 41), (39, 40), (40, 39)],
]
for wl in wind_lines:
    for i in range(len(wl) - 1):
        x1, y1 = wl[i]
        x2, y2 = wl[i+1]
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            gx = round(x1 + (x2 - x1) * s / steps)
            gy = round(y1 + (y2 - y1) * s / steps)
            draw_scaled_pixel(sheet, 128, 27*32, gx, gy-1, OUTLINE)
            draw_scaled_pixel(sheet, 128, 27*32, gx, gy+1, OUTLINE)
    for i in range(len(wl) - 1):
        x1, y1 = wl[i]
        x2, y2 = wl[i+1]
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            gx = round(x1 + (x2 - x1) * s / steps)
            gy = round(y1 + (y2 - y1) * s / steps)
            draw_scaled_pixel(sheet, 128, 27*32, gx, gy, CLD_LIGHT_HI)

sheet.save('tilesets/custom_home_items.png')

tsx_content = """<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="custom_home_items" tilewidth="32" tileheight="32" tilecount="240" columns="8">
 <image source="custom_home_items.png" width="256" height="960"/>
</tileset>
"""
with open('tilesets/custom_home_items.tsx', 'w') as f:
    f.write(tsx_content)

# Also export standalone 128x96 PNGs to ha_floorplan/ so Home Assistant can dynamically swap them by weather.home state!
ha_dir = 'www'
weather_crops = {
    'weather_sunny.png':        (0,   18*32, 128, 21*32),
    'weather_clear_night.png':  (128, 18*32, 256, 21*32),
    'weather_partlycloudy.png': (0,   21*32, 128, 24*32),
    'weather_cloudy.png':       (128, 21*32, 256, 24*32),
    'weather_rainy.png':        (0,   24*32, 128, 27*32),
    'weather_lightning.png':    (128, 24*32, 256, 27*32),
    'weather_fog.png':          (0,   27*32, 128, 30*32),
    'weather_windy.png':        (128, 27*32, 256, 30*32),
}
for fname, box in weather_crops.items():
    sheet.crop(box).save(f'{ha_dir}/{fname}')

# Render a preview of all 8 4x3 weather tiles on the exact sky blue background (152, 208, 248) & night sky (18, 24, 48)!
prev = Image.new('RGBA', (256*2, 384*2), (152, 208, 248, 255))
# Paint top-right (clear-night) background dark night blue so the moon & stars pop!
from PIL import ImageDraw
d = ImageDraw.Draw(prev)
d.rectangle([256, 0, 512, 192], fill=(18, 24, 48, 255))
w_part = sheet.crop((0, 18*32, 256, 30*32)).resize((512, 768), Image.NEAREST)
prev.alpha_composite(w_part, (0, 0))
prev.save('/tmp/preview_weather_tiles.png')
print("Generated 8 4x3 weather tile blocks and standalone HA PNGs!")

# Enhance raindrops on rainy & lightning so they pop against both day sky (#98D0F8) and night sky (#121830)!
for x_off, r_list in [
    (0,   [(16, 31), (24, 32), (32, 31), (40, 32), (48, 31), (19, 38), (27, 39), (35, 38), (43, 39)]),
    (128, [(15, 31), (22, 32), (41, 31), (48, 32), (18, 38), (44, 39)])
]:
    for rx, ry in r_list:
        for step in range(4):
            gx, gy = rx - step, ry + step
            draw_scaled_pixel(sheet, x_off, 24*32, gx + 1, gy, OUTLINE)
            draw_scaled_pixel(sheet, x_off, 24*32, gx, gy, BOLT_WHT if step == 0 else RAIN_LIGHT)

sheet.save('tilesets/custom_home_items.png')
for fname, box in weather_crops.items():
    sheet.crop(box).save(f'{ha_dir}/{fname}')

prev = Image.new('RGBA', (256*2, 384*2), (152, 208, 248, 255))
d = ImageDraw.Draw(prev)
d.rectangle([256, 0, 512, 192], fill=(18, 24, 48, 255))
w_part = sheet.crop((0, 18*32, 256, 30*32)).resize((512, 768), Image.NEAREST)
prev.alpha_composite(w_part, (0, 0))
prev.save('/tmp/preview_weather_tiles.png')

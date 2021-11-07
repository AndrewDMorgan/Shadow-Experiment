from Packages.PyVectors import *
import pygame, time

pygame.init()

class UI:
    # rendering text with many options (transparecy, size, centering, color, font, ect...)
    def text(text: str, color, pos, size: float, center: bool = False, font: str = 'pixel.ttf', trans: int = 255):
        largeText = pygame.font.Font(font, size)
        textSurface = largeText.render(text, True, color)
        TextSurf, TextRect = textSurface, textSurface.get_rect()
        if trans != 255:  # checking if the text is transparent
            surf = pygame.Surface(TextRect.size)
            if color == (0, 0, 0):  # making sure black text still works with transparecy
                surf.fill((255, 255, 255))
                surf.set_colorkey((255, 255, 255))
            else:
                surf.fill((0, 0, 0))
                surf.set_colorkey((0, 0, 0))
            surf.set_alpha(trans)
            n_pos = pos
            if center:  # checking if the text should be centered
                pos = (TextRect.size[0] // 2, TextRect.size[1] // 2)
            else:
                pos = (0, 0)
        else:
            surf = screen
        if center:  # checking if the text should be centered
            TextRect.center = pos
            sprite = surf.blit(TextSurf, TextRect)
        else:
            sprite = surf.blit(TextSurf, pos)
        
        if trans != 255:  # a bit more with transparecy
            if center:
                screen.blit(surf, (n_pos[0] - TextRect.size[0] // 2, n_pos[1] - TextRect.size[1] // 2))
            else:
                screen.blit(surf, n_pos)
        return sprite


# transparent polygon
def RenderTransparentPoly(color: Vec3, verts: List[Vec2], trans: int) -> None:
        min_x = 99999999999
        min_y = 99999999999
        max_x = -99999999999
        max_y = -99999999999
        for vert in verts:
            min_x = min(vert.x, min_x)
            min_y = min(vert.y, min_y)
            max_x = max(vert.x, max_x)
            max_y = max(vert.y, max_y)
        
        dif_x = math.ceil(max_x - min_x)
        dif_y = math.ceil(max_y - min_y)

        surf = pygame.Surface((dif_x + 2, dif_y + 2))
        solid_color = (0, 0, 0)
        if color[0] + color[1] + color[2] == 0:
            solid_color = (255, 255, 255)
        surf.fill(solid_color)
        surf.set_colorkey(solid_color)
        surf.set_alpha(trans)
        # add clipping
        poses = []
        for vert in verts:
            pos = (round(vert.x - min_x + 1), round(vert.y - min_y + 1))
            poses.append(pos)
        pygame.draw.polygon(surf, color, poses)
        screen.blit(surf, (min_x - 1, min_y - 1))


class Block:
    def __init__(self, pos: Vec2, size: Vec2, texture, shadow: bool = True) -> None:
        self.texture = texture
        self.size = size
        self.pos = pos
        self.shadow = shadow
        if not self.shadow:
            self.RenderShadow = lambda surf: 0
    def __ShadowRenderer(self, surf: pygame.Surface) -> None:
        if sun_dir < 90:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y), Vec2(self.pos.x, self.pos.y)]
        elif sun_dir == 90:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y), Vec2(self.pos.x, self.pos.y)]
        else:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y), Vec2(self.pos.x, self.pos.y + self.size.y)]
        
        if sun_dir < 90:
            tan_sun = math.tan((90 - sun_dir) / 180 * math.pi)
            final1 = Vec2(points[0].x - (res.y - points[0].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            final2 = Vec2(points[1].x - (res.y - points[1].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            points.append(final2)
            points.append(final1)
        else:
            tan_sun = math.tan((sun_dir - 90) / 180 * math.pi)
            final1 = Vec2(points[0].x + (res.y - points[0].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            final2 = Vec2(points[1].x + (res.y - points[1].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            points.append(final2)
            points.append(final1)
        #RenderTransparentPoly((125, 125, 125), points, shadow_trans)
        pygame.draw.polygon(surf, shadow_color, points)
    def GetShadowRenderer(self) -> None:
        self.RenderShadow = self.__ShadowRenderer
    def RenderShadow(self, surf: pygame.Surface) -> None:
        if sun_dir < 90:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y), Vec2(self.pos.x, self.pos.y)]
        elif sun_dir == 90:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y), Vec2(self.pos.x, self.pos.y)]
        else:
            points = [Vec2(self.pos.x + self.size.x, self.pos.y), Vec2(self.pos.x, self.pos.y + self.size.y)]
        
        if sun_dir < 90:
            tan_sun = math.tan((90 - sun_dir) / 180 * math.pi)
            final1 = Vec2(points[0].x - (res.y - points[0].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            final2 = Vec2(points[1].x - (res.y - points[1].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            points.append(final2)
            points.append(final1)
        else:
            tan_sun = math.tan((sun_dir - 90) / 180 * math.pi)
            final1 = Vec2(points[0].x + (res.y - points[0].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            final2 = Vec2(points[1].x + (res.y - points[1].y) * tan_sun, res.y)  # finding the position where the shadow hits the bottom of the screen
            points.append(final2)
            points.append(final1)
        #RenderTransparentPoly((125, 125, 125), points, shadow_trans)
        pygame.draw.polygon(surf, shadow_color, points)
    def Render(self) -> None:
        #pygame.draw.rect(screen, self.color, [self.pos.x, self.pos.y, self.size.x, self.size.y])
        screen.blit(self.texture, self.pos)


def GetTextures(atles_name: str, block_size: Vec2, blocks: Vec2) -> List[any]:
    atles = pygame.image.load(atles_name)
    final_atles = []
    for y in range(blocks.y):
        for x in range(blocks.x):
            index = Vec2(x, y)
            pos = block_size * index
            surf = pygame.Surface((block_size.x, block_size.y))
            surf.blit(atles, -pos)
            #surf.convert()
            surf.set_colorkey((0, 0, 0))
            final_atles.append(surf)
    return final_atles


# colors
shadow_color = Vec3(0, 0, 0)
shadow_trans = 75

background_color = Vec3(225, 225, 255)

# other variables
sun_dir = 45

# grass 0, dirt 1, stone 2, iron 3, coal 4, log 5, leavs 6, top water 7, bottom water 8, sand 9
textures = GetTextures('blocks.png', Vec2(10, 10), Vec2(5, 2))

surface_noise = lists.round1D(lists.map1D(array([120], 'perlin', [[-1, 1, 30, 'add'], [-0.5, 0.5, 15, 'add'], [-0.25, 0.25, 7.5, 'add']]), 40, 55))
cave_noise = lists.map2D(array([120, 750], 'perlin', [[-1, 1, 10, 'add'], [-0.5, 0.5, 5, 'add'], [-0.25, 0.25, 2.5, 'add']]), 0, 1)

for x in range(120):
    for y in range(75):
        dif = surface_noise[x] - 4 - y
        if dif >= 0 and dif <= 6:
            cave_noise[x][y] -= 1 - dif / 6
        if dif <= 0:
            cave_noise[x][y] = 0

cave_noise = lists.round2D(cave_noise)

air_posses = []
for x in range(120):
    layer = []
    for y in range(75):
        has_air = False
        if y >= surface_noise[x] - 1:
            has_air = True
        else:
            points = [
                cave_noise[min(x + 1, 119)][y],
                cave_noise[max(x - 1, 0)][y],
                cave_noise[x][min(y + 1, 74)],
                cave_noise[x][max(y - 1, 0)]
            ]
            for point in points:
                if point > 0:
                    has_air = True
                    break
        layer.append(has_air)
    air_posses.append(layer)

tree_spots = []
last_tree = 0
for x in range(120):
    if x - last_tree > 3 and surface_noise[x] >= 45 and x < 72:
        if random.randint(0, 3) == 0:
            tree_spots.append(x)
            last_tree = x

block_size = Vec2(10, 10)
block_array = array([120, 75], 'constant', None)
for x in range(120):
    for y in range(75):
        pos = Vec2(x, 74 - y) * Vec2(10, 10)
        is_air = air_posses[x][y]
        if y < surface_noise[x]:
            if cave_noise[x][y] <= 0:
                if surface_noise[x] - y <= 1:
                    if y < 44:
                        block_array[x][y] = (Block(pos, block_size, textures[9], is_air))
                    else:
                        block_array[x][y] = (Block(pos, block_size, textures[0], is_air))
                elif surface_noise[x] - y <= 3:
                    block_array[x][y] = (Block(pos, block_size, textures[1], is_air))
                else:
                    block_array[x][y] = (Block(pos, block_size, textures[2], is_air))
        elif y < 44:
            if y == 53:
                block_array[x][y] = (Block(pos, block_size, textures[7], False))
            else:
                block_array[x][y] = (Block(pos, block_size, textures[8], False))

for x in tree_spots:
    height = random.randint(4, 6)
    for y_ in range(height):
        y = y_ + surface_noise[x]
        block_array[x][y] = Block(Vec2(x * 10, (74 - y) * 10), block_size, textures[5])
    y = height + surface_noise[x]
    block_array[x - 1][y] = Block(Vec2(x * 10 - 10, (74 - y) * 10), block_size, textures[6])
    block_array[x    ][y] = Block(Vec2(x * 10     , (74 - y) * 10), block_size, textures[6])
    block_array[x + 1][y] = Block(Vec2(x * 10 + 10, (74 - y) * 10), block_size, textures[6])
    y -= 1
    block_array[x - 1][y] = Block(Vec2(x * 10 - 10, (74 - y) * 10), block_size, textures[6])
    block_array[x    ][y] = Block(Vec2(x * 10     , (74 - y) * 10), block_size, textures[6])
    block_array[x + 1][y] = Block(Vec2(x * 10 + 10, (74 - y) * 10), block_size, textures[6])
    y -= 1
    block_array[x - 2][y] = Block(Vec2(x * 10 - 20, (74 - y) * 10), block_size, textures[6])
    block_array[x - 1][y] = Block(Vec2(x * 10 - 10, (74 - y) * 10), block_size, textures[6])
    block_array[x + 1][y] = Block(Vec2(x * 10 + 10, (74 - y) * 10), block_size, textures[6])
    block_array[x + 2][y] = Block(Vec2(x * 10 + 20, (74 - y) * 10), block_size, textures[6])
    y -= 1
    block_array[x - 2][y] = Block(Vec2(x * 10 - 20, (74 - y) * 10), block_size, textures[6])
    block_array[x - 1][y] = Block(Vec2(x * 10 - 10, (74 - y) * 10), block_size, textures[6])
    block_array[x + 1][y] = Block(Vec2(x * 10 + 10, (74 - y) * 10), block_size, textures[6])
    block_array[x + 2][y] = Block(Vec2(x * 10 + 20, (74 - y) * 10), block_size, textures[6])

# screen
res = Vec2(1200, 750)
screen = pygame.display.set_mode(res)

dt = 0

shadow_surf = pygame.Surface(res)
shadow_surf.fill(background_color)
shadow_surf.set_alpha(shadow_trans)
for x in range(120):
    for y in range(75):
        if block_array[x][y] is not None:
            block_array[x][y].RenderShadow(shadow_surf)

mouse_held = False
mouse_held_right = False

# main loop
running = True

while running:
    s = time.time()
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sun_dir -= 15
                sun_dir = max(sun_dir, 1)

                shadow_surf = pygame.Surface(res)
                shadow_surf.fill(background_color)
                shadow_surf.set_alpha(shadow_trans)
                for x in range(120):
                    for y in range(75):
                        if block_array[x][y] is not None:
                            block_array[x][y].RenderShadow(shadow_surf)
            if event.key == pygame.K_RIGHT:
                sun_dir += 15
                sun_dir = min(sun_dir, 179)

                shadow_surf = pygame.Surface(res)
                shadow_surf.fill(background_color)
                shadow_surf.set_alpha(shadow_trans)
                for x in range(120):
                    for y in range(75):
                        if block_array[x][y] is not None:
                            block_array[x][y].RenderShadow(shadow_surf)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_held = True
            elif event.button == 3:
                mouse_held_right = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_held = False
            elif event.button == 3:
                mouse_held_right = False
    
    if not running:
        pygame.quit()
        break
    
    try:
        if mouse_held:
            block_pos = pygame.mouse.get_pos()
            block_pos = floor(Vec2(block_pos[0], block_pos[1]) / block_size)
            block_pos.y = 74 - block_pos.y
            
            if block_array[block_pos.x][block_pos.y] is not None:
                block_array[block_pos.x][block_pos.y] = None
                try:
                    block_array[block_pos.x - 1][block_pos.y].shadow = True
                    block_array[block_pos.x - 1][block_pos.y].GetShadowRenderer()
                except IndexError and AttributeError:
                    pass
                try:
                    block_array[block_pos.x + 1][block_pos.y].shadow = True
                    block_array[block_pos.x + 1][block_pos.y].GetShadowRenderer()
                except IndexError and AttributeError:
                    pass
                try:
                    block_array[block_pos.x][block_pos.y - 1].shadow = True
                    block_array[block_pos.x][block_pos.y - 1].GetShadowRenderer()
                except IndexError and AttributeError:
                    pass
                try:
                    block_array[block_pos.x][block_pos.y + 1].shadow = True
                    block_array[block_pos.x][block_pos.y + 1].GetShadowRenderer()
                except IndexError and AttributeError:
                    pass
            
                shadow_surf = pygame.Surface(res)
                shadow_surf.fill(background_color)
                shadow_surf.set_alpha(shadow_trans)
                for x in range(120):
                    for y in range(75):
                        if block_array[x][y] is not None:
                            block_array[x][y].RenderShadow(shadow_surf)
        elif mouse_held_right:
            block_pos = pygame.mouse.get_pos()
            block_pos = floor(Vec2(block_pos[0], block_pos[1]) / block_size)
            block_pos.y = 74 - block_pos.y

            if block_array[block_pos.x][block_pos.y] is None:
                block_array[block_pos.x][block_pos.y] = Block(Vec2(block_pos.x, 74 - block_pos.y) * block_size, block_size, textures[2])

                shadow_surf = pygame.Surface(res)
                shadow_surf.fill(background_color)
                shadow_surf.set_alpha(shadow_trans)
                for x in range(120):
                    for y in range(75):
                        if block_array[x][y] is not None:
                            block_array[x][y].RenderShadow(shadow_surf)
    except IndexError:
        pass
    
    # random ticks
    for tick in range(12):
        pos = Vec2(random.randint(0, 119), random.randint(0, 74))
        if block_array[pos.x][pos.y] is not None:
            texture_index = textures.index(block_array[pos.x][pos.y].texture)
            if texture_index == 0:  # grass blocks
                con = True
                if block_array[pos.x][pos.y + 1] is not None:
                    if textures.index(block_array[pos.x][pos.y].texture) != 6:
                        con = False

                if not con:
                    block_array[pos.x][pos.y] = Block(Vec2(pos.x, 74 - pos.y) * block_size, block_size, textures[1], block_array[pos.x][pos.y].shadow)
            elif texture_index == 1:  # dirt blocks
                try:
                    con = True
                    if block_array[pos.x][pos.y + 1] is not None:
                        if textures.index(block_array[pos.x][pos.y].texture) != 6:
                            con = False
                    
                    if con:
                        t1 = False
                        t2 = False
                        t3 = False
                        t4 = False
                        try:
                            t1 = textures.index(block_array[pos.x - 1][pos.y].texture) == 0
                        except IndexError and AttributeError:
                            pass
                        try:
                            t2 = textures.index(block_array[pos.x + 1][pos.y].texture) == 0
                        except IndexError and AttributeError:
                            pass
                        try:
                            t3 = textures.index(block_array[pos.x - 1][pos.y + 1].texture) == 0
                        except IndexError and AttributeError:
                            pass
                        try:
                            t4 = textures.index(block_array[pos.x + 1][pos.y + 1].texture) == 0
                        except IndexError and AttributeError:
                            pass
                        
                        if (t1 or t2 or t3 or t4):# and random.randint(0, 0) == 0:
                            block_array[pos.x][pos.y] = Block(Vec2(pos.x, 74 - pos.y) * block_size, block_size, textures[0], block_array[pos.x][pos.y].shadow)
                except IndexError:
                    pass

    screen.fill(background_color)

    screen.blit(shadow_surf, (0, 0))
    
    for x in range(120):
        for y in range(75):
            if block_array[x][y] is not None:
                block_array[x][y].Render()

    UI.text(f'FPS: {round(1 / max(dt, 0.00000001), 2)}', (0, 0, 15), (10, 10), 25)

    pygame.display.update()

    e = time.time()
    dt = e - s


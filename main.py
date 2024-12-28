import pygame, string, random
import yaml

# Load data 
def load_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data['sentences']

sentences = load_sentences('data/file01.yml')
number_of_sentences = len(sentences)
sentence_idx = random.sample(range(0, number_of_sentences), number_of_sentences)

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Learn English by Typing!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

display_surface.fill(BLACK)

FPS = 60

se_correct = pygame.mixer.Sound("sound/meka_ka_type02.mp3")
se_correct.set_volume(0.7)

alphabet_lowercase = string.ascii_lowercase
alphabet_uppercase = string.ascii_uppercase

class Game():
    def __init__(self):

        self.typing_text = []

        self.key_input_index = 0

        self.correct_number = 0

        self.wrong_number = 0

        self.next_sentence_idx = 0

        self.next_sentence_length = 0

        # (50, 80, WINDOW_WIDTH - 100, 250): The position and size of the rectangle.
        # The rectangle's top-left corner is at (50, 80), its width is WINDOW_WIDTH - 100 (which is 700 pixels), 
        # and its height is 250 pixels.
        pygame.draw.rect(display_surface, WHITE, (50, 80, WINDOW_WIDTH - 100, 250), 5)

        self.font_25 = pygame.font.Font('NotoSansJP-VariableFont_wght.ttf', 25)
        self.font_40 = pygame.font.Font('NotoSansJP-VariableFont_wght.ttf', 40)
        self.font_55 = pygame.font.Font('NotoSansJP-VariableFont_wght.ttf', 55)
        # sentence size
        self.font_10 = pygame.font.Font('NotoSansJP-VariableFont_wght.ttf', 10)

        self.point, self.point_rect = self.text_board(self.font_25, "正解した文字数: ", WHITE)
        self.missing, self.missing_rect = self.text_board(self.font_25, "間違えた文字数: ", WHITE)
        self.key_input, self.key_input_rect = self.text_board(self.font_40, "入力されたキー: ", WHITE)

        # Position
        self.point_rect.center = (WINDOW_WIDTH // 2 - 200, 30)
        self.missing_rect.center = (WINDOW_WIDTH // 2 + 150, 30)
        self.key_input_rect.center = (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100)

        

        display_surface.blit(self.point, self.point_rect)
        display_surface.blit(self.missing, self.missing_rect)
        display_surface.blit(self.key_input, self.key_input_rect)

        self.score_text_create()

    def text_board(self, font, text, color):
        # font = pygame.font.Font(font, size)
        textsurf = font.render(text, True, color)
        textsurf_rect = textsurf.get_rect()
        return (textsurf, textsurf_rect)
    
    def input_key_now(self, s):
        # pygame.draw.rect(display_surface, BLACK, (480, 365, 80, 80))
        pygame.draw.rect(display_surface, BLACK, (WINDOW_WIDTH // 2 + 50, WINDOW_HEIGHT - 120, 200, 80))

        inputKey, inputKey_rect = self.text_board(self.font_40, s, WHITE)
        inputKey_rect.center = (WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT - 100)
        display_surface.blit(inputKey, inputKey_rect)

    def next_sentence_load(self):
    # if out of index, return
        if self.next_sentence_idx >= number_of_sentences:
            return

        self.typing_text = list(sentences[self.next_sentence_idx]['english'])
        self.next_sentence_length = len(self.typing_text)

        # increment the index
        self.next_sentence_idx += 1

    def display_typing_text(self):
        text, text_rect = self.text_board(self.font_25, ''.join(self.typing_text), WHITE)
        text_rect.center = (WINDOW_WIDTH // 2, 200)
        display_surface.blit(text, text_rect)

    def key_input_check(self, key_):
        if self.typing_text[self.key_input_index] == key_:
            self.typing_text[self.key_input_index] = ''

            if self.next_sentence_length == self.key_input_index:
                exit()
            else:
                self.key_input_index += 1

            pygame.draw.rect(display_surface, BLACK, (60, 90, WINDOW_WIDTH - 120, 230))
            # pygame.draw.rect(display_surface, BLACK, (60, 90, WINDOW_WIDTH - 120, 500))

            self.display_typing_text()

            self.correct_number += 1
        else:
            self.wrong_number +=1

    def score_text_create(self):
        pygame.draw.rect(display_surface, BLACK, (self.point_rect.x + self.point_rect.width + 10, \
                                                  self.point_rect.y, 50, 50))
        pygame.draw.rect(display_surface, BLACK, (self.missing_rect.x + self.missing_rect.width + 10, \
                                                  self.missing_rect.y, 50, 50))
        correct, correct_rect = self.text_board(self.font_25, str(self.correct_number), WHITE)
        wrong, wrong_rect = self.text_board(self.font_25, str(self.wrong_number), WHITE)

        correct_rect.topleft = (self.point_rect.x + self.point_rect.width + 10, self.point_rect.y)
        wrong_rect.topleft = (self.missing_rect.x + self.missing_rect.width + 10, self.missing_rect.y)

        display_surface.blit(correct, correct_rect)
        display_surface.blit(wrong, wrong_rect)

    def gameInitCheck(self):
        if self.key_input_index == len(self.typing_text):
            self.key_input_index = 0
            self.typing_text = []
            self.correct_number = self.wrong_number = 0

            self.input_key_now('')
            self.next_sentence_load()
            self.display_typing_text()

game = Game()

game.next_sentence_load()
game.display_typing_text()

running = True
clock = pygame.time.Clock()

while running:
    # detect key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not ((97 <= event.key <= 122) or event.key in [pygame.K_SPACE, pygame.K_COMMA, pygame.K_PERIOD, 
                                                         pygame.K_EXCLAIM, pygame.K_QUESTION, pygame.K_COLON, 
                                                         pygame.K_SEMICOLON]):
                continue
            se_correct.play()
            key_name = pygame.key.name(event.key).upper()
            if key_name == 'SPACE':
                key_name = ' '
                game.key_input_check(key_name)
                continue
            # if Shift is held down
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                game.input_key_now(pygame.key.name(event.key).upper())
                game.key_input_check(pygame.key.name(event.key).upper())
            else:
                game.input_key_now(pygame.key.name(event.key))
                game.key_input_check(pygame.key.name(event.key))
            game.gameInitCheck()
        game.score_text_create()
    clock.tick(FPS)

    # Refresh the display to make any changes visible
    pygame.display.update()

pygame.quit()




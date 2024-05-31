import pygame
import random
import copy

pygame.init()

i_max = 11  #переменные чтобы задать сетку
j_max = 21

screen_x = 300 #переменный с параметрами экрана
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y)) # Окно игры
clock = pygame.time.Clock() #  частота обновления кадров для работы со вреиенем

dx = screen_x/(i_max-1) #ширина и высота ячейки
dy = screen_y/(j_max-1)

fps = 60
grid= []  #список для параметра сетки

# параметры сетки
def init_grid():
    global grid
    grid = []
    for i in range(0, i_max):
        grid.append([])
        for j in range(0, j_max):
            grid[i].append([1]) # Состояние ячейки (1 - пустая, 0 - занятая)
            grid[i][j].append(pygame.Rect(i * dx, j * dy, dx, dy))  # Прямоугольник, представляющий ячейку
            grid[i][j].append(pygame.Color("Gray"))

details = [
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    [[1, 0], [1, 1], [0, 0], [-1, 0]],
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

det = [[], [], [], [], [], [], []] #список с самими деталями, заполняем сущностью 4 прямоугольнков( 1 деталь= 4 квадратам)
for i in range(0, len(details)):
    for j in range(0, 4):
        det[i].append(pygame.Rect(details[i][j][0]*dx + dx*(i_max//2), details[i][j][1]*dy, dx, dy))

detail = pygame.Rect(0, 0, dx, dy) # Прямоугольник для отрисовки деталей
det_choice = copy.deepcopy(random.choice(det))


# Функция для сброса игры
def reset_game():
    global det_choice, count, rotate, game_over, fall_speed, score
    init_grid()  # Инициализация сетки
    det_choice = copy.deepcopy(random.choice(det))  # Выбор случайной детали
    count = 0  # Счетчик для управления скоростью падения деталей
    rotate = False  # Флаг для поворота детали
    game_over = False  # Флаг окончания игры
    fall_speed = 31 * fps  # Начальная скорость падения
    score = 0 #счёт игры

reset_game()  # Сброс игры перед началом
font = pygame.font.SysFont("Arial", 30)  # Шрифт для текста
game_over_text = font.render("GAME OVER", True, pygame.Color("Red"))  # Текст "GAME OVER"
game_over_rect = game_over_text.get_rect(center=(screen_x // 2, screen_y // 2 - 50))  # Прямоугольник для текста "GAME OVER"
retry_text = font.render("Try again", True, pygame.Color("Black"))  # Текст "Повторить попытку"
retry_rect = retry_text.get_rect(center=(screen_x // 2, screen_y // 2 + 50))  # Прямоугольник для кнопки "Повторить попытку"
score_text = font.render(f"Score: {score}", True, pygame.Color("White"))  # Текст для счета
score_rect = score_text.get_rect(center=(screen_x // 2, 30))  # Прямоугольник для счета
start_button = font.render("Start Game", True, pygame.Color("White"))
start_button_rect = start_button.get_rect(center=(screen_x // 2, screen_y // 2))

game = True  # Флаг выхода из игрового цикла
count = 0  # Счетчик для управления скоростью падения деталей
rotate = False  # Флаг для поворота детали
in_main_menu = True

while game:  # Основной игровой цикл
    if in_main_menu:
        screen.fill(pygame.Color("Black"))
        pygame.draw.rect(screen, pygame.Color("Blue"), start_button_rect.inflate(20, 10))
        screen.blit(start_button, start_button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    in_main_menu = False

    else:
        sdvig_x = 0  # Сдвиг по горизонтали
        sdvig_y = 1  # Сдвиг по вертикали

        if game_over:  # Если игра окончена

            pygame.draw.rect(screen, pygame.Color("White"), retry_rect.inflate(20, 10))  # Рисуем белый фон для кнопки
            pygame.draw.rect(screen, pygame.Color("Black"), game_over_rect.inflate(20, 10))
            screen.blit(game_over_text, game_over_rect)
            screen.blit(retry_text, retry_rect)  # Отображение кнопки "Повторить попытку"
            pygame.display.flip()  # Обновление экрана

            for event in pygame.event.get():  # Обработка событий
                if event.type == pygame.QUIT:  # Закрытие окна
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие кнопки мыши
                    if retry_rect.collidepoint(event.pos):  # Если нажата кнопка "Повторить попытку"
                        reset_game()  # Сброс игры
            continue  # Переход к следующей итерации цикла

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Закрытие окна
                exit()
            if event.type == pygame.KEYDOWN:  # Нажатие клавиши
                if event.key == pygame.K_LEFT or event.key == ord('a'):  # Влево
                    sdvig_x = -1
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):  # Вправо
                    sdvig_x = 1
                elif event.key == pygame.K_UP or event.key == ord('w'):  # Поворот
                    rotate = True
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:  # Ускорение падения детали
            count = fall_speed

        screen.fill(pygame.Color("Black"))  # Заливка фона черным цветом

        for i in range(0, i_max):  # Отрисовка сетки
            for j in range(0, j_max):
                pygame.draw.rect(screen, grid[i][j][2], grid[i][j][1], grid[i][j][0])  # Отрисовка ячейки


        # Функция для проверки столкновений и выхода за границы поля
        colors_for_det=random.choice([pygame.Color("Yellow"), pygame.Color("Red"), pygame.Color("Green"),pygame.Color("Blue")])
        for i in range(4): # огр поля
            if ((det_choice[i].x + sdvig_x*dx < 0) or (det_choice[i].x + sdvig_x*dx >=screen_x)):
                sdvig_x = 0
            if ((det_choice[i].y+ dy >= screen_y) or grid[int(det_choice[i].x // dx)][int(det_choice[i].y // dy +1)][0] == 0):
                sdvig_y =0
                for i in range(4):
                    x = int(det_choice[i].x // dx)
                    y = int(det_choice[i].y // dy)
                    grid[x][y][0] = 0 #закрашиваем квадратик
                    grid[x][y][2] = colors_for_det


                detail_x = 0
                detail_y = 0
                det_choice = copy.deepcopy(random.choice(det))
                colors_for_det = random.choice([pygame.Color("Yellow"), pygame.Color("Red"), pygame.Color("Green"), pygame.Color("Blue")])
                break


        for i in range(4): #движение случайной детали по х
            det_choice[i].x += sdvig_x*dx

        count += fps
        if count>31 *fps:
            for i in range(4):
                det_choice[i].y += sdvig_y*dy
            count=0 # замедлить движение

        for i in range(4): #отрисовка нашей детали в программе
            detail.x = det_choice[i].x
            detail.y = det_choice[i].y
            pygame.draw.rect(screen, pygame.Color("White"), detail)

        C = det_choice[2] # центр
        if rotate == True:
            for i in range(4):
                x = det_choice[i].y - C.y
                y = det_choice[i].x - C.x

                det_choice[i].x = C.x - x
                det_choice[i].y = C.y + y
            rotate = False

        for j in range(j_max - 1, -1, -1):  # цикл снизу вверх
            count_cells = 0
            for i in range(0, i_max):  # цикл по столбцам справа налево
                if grid[i][j][0] == 0:  # если ячейка закрашена
                    count_cells += 1
                elif grid[i][j][0] == 1:  # если ячейка пустая
                    break
            if count_cells == (i_max - 1):  # если строка полностью заполнена
                score += 10
                for l in range(0, i_max):
                    grid[l][0][0] = 1  # устанавливаем ячейку пустой
                    grid[l][0][2] = pygame.Color("Gray")  # устанавливаем цвет серым
                for k in range(j, -1, -1):
                    for l in range(0, i_max):
                        grid[l][k][0] = grid[l][k - 1][0]  # сдвиг состояния ячейки
                        grid[l][k][2] = grid[l][k - 1][2]  # сдвиг цвета ячейки
                for l in range(0, i_max):
                    grid[l][0][2] = pygame.Color("Gray")  # после сдвига верхняя строка устанавливается серой


        if any(grid[i][0][0] == 0 for i in range(i_max)):
            game_over = True

        score_text = font.render(f"Score: {score}", True, pygame.Color("White"))  # Обновление текста счета
        screen.blit(score_text, score_rect)

        pygame.display.flip() #контролирует, когда и как изменения, внесенные в ваш код, будут видны на экране.
        clock.tick(fps) # ограничение на частоту кадров тик, чтобы не перегрузить комп
pygame.quit()



import pygame
import sys
import random

# Pantalla
ANCHO, ALTO = 600, 400

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_COMIDA = (255, 0, 0)

# sNAKE

class Snake:
    def __init__(self):
        self.body = [(100, 50), (90, 50), (80, 50)]
        self.direccion = "DERECHA"
        self.crecer = False

    def mover(self):
        x, y = self.body[0] # obtengo la posición de la cabeza
        if self.direccion == "DERECHA":
            x += 10
        elif self.direccion == "IZQUIERDA":
            x -= 10
        elif self.direccion == "ARRIBA":
            y -= 10
        elif self.direccion == "ABAJO":
            y += 10
        # Genero la nueva cabeza con la posición 
        nueva_cabeza = (x, y)
        self.body.insert(0, nueva_cabeza)
        # Si no se debe crecer, elimino el último segmento
        if not self.crecer:
            self.body.pop()
        else:
            self.crecer = False

    def change_direction(self, new_direction):
        if new_direction == "ARRIBA" and self.direccion != "ABAJO":
            self.direccion = new_direction
        elif new_direction == "ABAJO" and self.direccion != "ARRIBA":
            self.direccion = new_direction
        elif new_direction == "IZQUIERDA" and self.direccion != "DERECHA":
            self.direccion = new_direction
        elif new_direction == "DERECHA" and self.direccion != "IZQUIERDA":
            self.direccion = new_direction
        
    def eat(self):
        self.crecer = True

    def collision(self):
        head = self.body[0]
        # Colisión con bordes
        if head[0] < 0 or head[0] >= ANCHO or head[1] < 0 or head[1] >= ALTO:
            return True
        # Colisión con sí misma
        if head in self.body[1:]:
            return True
        return False

    def draw(self, ventana):
        for segment in self.body:
            pygame.draw.rect(ventana, COLOR_SNAKE, pygame.Rect(segment[0], segment[1], 10, 10))

class Food:
    def __init__(self):
        self.position = self.generate()

    def generate(self):
        x = random.randint(0, (ANCHO // 10) - 1) * 10
        y = random.randint(0, (ALTO // 10) - 1) * 10
        return (x, y)

    def draw(self, ventana):
        pygame.draw.rect(ventana, COLOR_COMIDA, pygame.Rect(self.position[0], self.position[1], 10, 10))

class Game:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Snake Game")
        self.fps = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.points = 0

    def check_food(self):
        if self.snake.body[0] == self.food.position:
            self.snake.eat()
            self.food.position = self.food.generate()
            self.points += 1

    def check_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                    self.snake.change_direction("ARRIBA")
                elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                    self.snake.change_direction("ABAJO")
                elif evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                    self.snake.change_direction("IZQUIERDA")
                elif evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                    self.snake.change_direction("DERECHA")

    def update(self):
        while True:
            self.check_events()
            self.snake.mover() 
            self.check_food()

            if self.snake.collision():
                print("Game Over")
                print(f"Puntos: {self.points}")
                pygame.quit()
                sys.exit()

            self.ventana.fill(COLOR_FONDO)
            self.snake.draw(self.ventana)
            self.food.draw(self.ventana)
            pygame.display.flip()
            self.fps.tick(15)

if __name__ == "__main__":
    juego = Game()
    juego.update()

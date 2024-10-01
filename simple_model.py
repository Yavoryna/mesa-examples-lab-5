from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt


class SimpleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)  # Виклик конструктора батьківського класу
        self.pos = (self.random.randrange(model.grid.width), self.random.randrange(model.grid.height))

    def step(self):
        x_move = self.random.choice([-1, 0, 1])  # Рух вліво, без руху, або вправо
        y_move = self.random.choice([-1, 0, 1])  # Рух вниз, без руху, або вгору

        new_x = (self.pos[0] + x_move) % self.model.grid.width
        new_y = (self.pos[1] + y_move) % self.model.grid.height

        self.model.grid.move_agent(self, (new_x, new_y))


class SimpleModel(Model):
    def __init__(self, N, width, height):
        super().__init__()  # Виклик конструктора батьківського класу
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)  # Розміри сітки
        self.schedule = RandomActivation(self)

        # Збирач даних
        self.datacollector = DataCollector(
            agent_reporters={"Position": lambda a: a.pos}  # Отримання позиції агента
        )

        # Додавання агентів
        for i in range(self.num_agents):
            a = SimpleAgent(i, self)
            self.schedule.add(a)
            # Використовуємо випадкову позицію агента під час ініціалізації
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.datacollector.collect(self)  # Збір даних перед кроком
        self.schedule.step()  # Крок усіх агентів

        # Вивід позицій агентів на консоль
        print(f"Step {self.schedule.time}:")
        for agent in self.schedule.agents:
            print(f"Agent {agent.unique_id} position: {agent.pos}")


if __name__ == "__main__":
    model = SimpleModel(10, 10, 10)
    steps_n = 100
    for i in range(steps_n):
        model.step()
    data = model.datacollector.get_agent_vars_dataframe()
    positions = data.loc[steps_n - 1, 'Position']
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    plt.scatter(x, y)
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.title("Позиції агентів після 100 кроків")
    plt.show()

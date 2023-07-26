from dlgo.agent.naive import RandomBot
from dlgo.httpfrontend.server import get_web_app
from dlgo.mcts import MCTSAgent

BOARD_SIZE = 5

def main():
    bot = MCTSAgent(700, temperature=1.4)

    web_app = get_web_app({'mcts': bot})
    web_app.run()

if __name__ == '__main__':
    main()
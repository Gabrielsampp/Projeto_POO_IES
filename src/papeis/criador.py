from src.quiz.quiz import Quiz


class Criador:
    def __init__(self):
        self._quizzes = []

    @property
    def quizzes(self):
        return tuple(self._quizzes)

    def adicionar_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            raise TypeError("É necessário fornecer um objeto Quiz.")

        if quiz in self._quizzes:
            raise ValueError("Esse Quiz já está associado ao criador.")

        if quiz.professor is not None and quiz.professor is not self:
            raise ValueError("Esse Quiz já pertence a outro professor.")

        quiz.professor = self
        self._quizzes.append(quiz)

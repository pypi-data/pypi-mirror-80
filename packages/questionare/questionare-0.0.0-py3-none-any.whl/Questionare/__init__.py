questions = []
Answers = []
ending = "Thank you for taking this quiz!"
def help():
        print("SubCommands:")
        print("-----------------------------------------")
        print("help - shows this help page")
        print("addQuestion - adds a question")
        print("deleteQuestion - removes a question")
        print("printQuestions - prints all existing questions")
        print("setFinishedText - sets the text users see what the survey finishes")
        print("start - starts the survey")
        print("answers - shows the answers")
        print("reset - resets all options")
        print("-----------------------------------------")
        print("Module created by CraftYun83")
def addQuestion(addQuestion):
        questions.append(addQuestion)
def printQuestions():
        print(questions)
def deleteQuestion(deleteQuestion):
        questions.remove(deleteQuestion)
        print("Deleted:" , deleteQuestion , "from questions!")
def setFinishedText(text):
        ending = text
def start():
        count = 0
        QuestionLength = len(questions)
        for i in range(QuestionLength):
                answer = input(questions[count])
                Answers.append(answer)
                count = count + 1
        print(ending)
        action = input()
        if action == "Answers":
                answers()
        if action == "printQuestions":
                printQuestions()
        if action == "reset":
                reset()
        if action == "start":
                start()
        if action == "help":
                help()
def answers():
        countAnswers = 0
        AnswersLength = len(Answers)
        print("Answers:")
        for i in range(AnswersLength):
                number = countAnswers + 1
                print(number , ":" , Answers[countAnswers])
                countAnswers = countAnswers + 1
def reset():
        questions = []
        count = 0
        answers = []
        ending = "Thank you for taking this quiz!"
        print("All settings has been resetted")
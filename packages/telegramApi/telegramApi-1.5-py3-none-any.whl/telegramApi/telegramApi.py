import telegram, configparser, os

class telegramApi:
    def __init__(self,pathToIni):
        self.config = configparser.ConfigParser()
        self.setConfig(pathToIni)
        self.__bot = None
        self.__chatId = ""
        self.setBotConfig()

    def setConfig(self,pathToIni):
        if os.path.exists(pathToIni):
            try:
                self.config.read(pathToIni)
            except Exception as e:
                print("Nao foi possivel carregar a configuracao. Exception:\n"+str(e))
        else:
            print("Nao foi possivel carregar a configuracao.\nArquivo nao encontrado!")

    def setBotConfig(self):
        defaultConfig = self.config['TELEGRAM']
        self.__bot = telegram.Bot(token=defaultConfig['bot.token'])
        self.__chatId = defaultConfig['chat.id']

    def sendMessage(self,message):
        self.__bot.send_message(chat_id=self.__chatId, text=message)
    
    #Receive string file path
    def sendFile(self,filePath):
        sendFile = open(filePath, 'rb')
        self.__bot.send_document(chat_id=self.__chatId, document=sendFile)
        sendFile.close()
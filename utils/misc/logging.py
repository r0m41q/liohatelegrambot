import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
                           u'[%(asctime)s] [%(threadName)-12.12s]  %(message)s',
                    level=logging.INFO,
                    handlers=[
                            logging.FileHandler("app.log"),
                            logging.StreamHandler()
                        ]
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

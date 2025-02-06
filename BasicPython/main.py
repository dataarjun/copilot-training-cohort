# TODO: Added logging to track user actions

# import logging
# logging.basicConfig(filename='app.log', level=logging.INFO)
# logging.info('Starting the application')
# print('Hello World')
# logging.info('Ending the application')


import logging

def main():
    logging.basicConfig(filename='app.log', level=logging.INFO)
    logging.info('Starting the application')
    print('Hello World')
    logging.info('Ending the application')

if __name__ == '__main__':
    main()  
    
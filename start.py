from traceback import print_tb
import speech_recognition as sr
import asyncio
import os
import re


async def rewrite_file_loop():
    seconds = int()
    name_sound_file = str(input('Укажите название файла: '))

    try:
        seconds = int(input('Укажите с какой секунды начать транскрибацию файла: '))
    except ValueError:
        print('Укажите числовое значение')
        return

    recog = sr.Recognizer()
    audioF = sr.AudioFile(os.path.join(os.path.abspath('./files/'), name_sound_file))
    
    name_text_file = rename_sound_to_text_file(name_sound_file)
    name_file = os.path.join(os.path.abspath('./transcribe/'), name_text_file)

    if name_sound_file != '':
        print('Начал выполнение для файла ' + name_sound_file)

        try:
            with audioF as source:   
                num_minute = seconds / 60

                audio = recog.record(source, duration=60, offset=seconds)
                write_transcribe_file(recog, name_file, audio)
                print("{} минута была записана в файл {}".format(int(num_minute), name_text_file))

                num_minute += 1

                while True:

                    try:
                        audio = recog.record(source, duration=60)

                        await asyncio.sleep(1)

                        write_transcribe_file(recog, name_file, audio)
                        
                        print("{} минута была записана в файл {}".format(num_minute, name_text_file))
                        num_minute += 1
                    
                    except sr.UnknownValueError:
                        print(f'Программа не смогла распознать файл {name_text_file} или запись окончена')
                        break

                    except sr.RequestError as err:
                        print(f'Не удалось получить результаты от службы распознавания речи Google - {err}')
        
        except ValueError as err:
            if 'Audio file could not be read as PCM WAV, AIFF/AIFF-C, or Native FLAC; check if file is corrupted or in another format' in err.args:
                print('Такой формат звукового файла не поддерживается [' + name_sound_file + ']')

        except FileNotFoundError:
            print('Файла с именем ' + name_sound_file + ' не существует')

    else:
        print('Вы указали неверное имя файла!')

async def main_loop(file):    
    recog = sr.Recognizer()
    audioF = sr.AudioFile(file)

    name_sound_file = os.path.basename(file)
    name_text_file = rename_sound_to_text_file(name_sound_file)
    name_file = os.path.abspath('./transcribe/') + name_text_file

    print('Начал выполнение для файла ' + name_sound_file)

    try:
        with audioF as source: 
            num_minute = 0              

            while True:

                try:
                    audio = recog.record(source, duration=60)

                    await asyncio.sleep(1)

                    num_minute += 1

                    write_transcribe_file(recog, name_file, audio)
                    
                    print("{} минута была записана в файл {}".format(num_minute, name_text_file))                    
                
                except sr.UnknownValueError:
                    print(f'Программа не смогла распознать файл {name_text_file} или запись окончена')
                    break

                except sr.RequestError as err:
                    print(f'Не удалось получить результаты от службы распознавания речи Google - {err}')
    
    except ValueError as err:
        if 'Audio file could not be read as PCM WAV, AIFF/AIFF-C, or Native FLAC; check if file is corrupted or in another format' in err.args:
            print('Такой формат звукового файла не поддерживается [' + name_sound_file + ']')


# Получение названия текстового файла из звукового
def rename_sound_to_text_file(sound_file):
    type_files_compile = re.compile(r".flac|.wav|.aiff$")
    name_text_file = ''

    if re.search(type_files_compile, sound_file) is not None:
        name_text_file = re.sub(type_files_compile, '.txt', sound_file)

    return name_text_file


# Запись данных в файл транскрибации
def write_transcribe_file(recog, text_file, audio_file):    
    if os.path.exists(text_file):
        with open(text_file, 'a', encoding='utf-8') as fin:
            fin.write(recog.recognize_google(audio_file, language="ru-RU") + "\n")
    else:
        with open(text_file, 'w', encoding='utf-8') as fin:
            fin.write(recog.recognize_google(audio_file, language="ru-RU") + "\n")


async def user_message():
    message = """Выберите что надо сделать:
    new - Выполнить транскрибацию всех файлов
    rewrite - Дописать остановленный файл
    """

    print(message)

    return input('Введите команду: ')


async def main():  
    user_choice = await user_message()

    # Транскрибация всех файлов
    if user_choice == 'new':
        tasks = []
        
        dirname = './files'
        dirfiles = os.listdir(dirname)

        fullpaths = map(lambda name: os.path.join(os.path.abspath(dirname), name), dirfiles)

        # Сбор всех звуковых файлов и создание задач
        for file in fullpaths:
            if '.DS_Store' not in file:
                if os.path.isfile(file): 
                    task = asyncio.create_task(main_loop(file))
                    tasks.append(task)

        await asyncio.gather(*tasks)

    # Транскрибация остановленного файла
    elif user_choice == 'rewrite':
        await rewrite_file_loop()

    # Выход из программы
    else:
        print('Exit programm')


if __name__ == '__main__':
    asyncio.run(main())
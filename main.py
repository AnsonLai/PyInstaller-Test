import requests
import json

import PySimpleGUI as sg

import sys
import os
if getattr(sys, 'frozen', False):
    Current_Path = os.path.dirname(sys.executable)
else:
    Current_Path = str(os.path.dirname(__file__))

def main():
  pokemon_list = []

  r = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1500')
  output = r.json()

  for pokemon in output['results']:
    pokemon_list.append(pokemon['name'].upper())

  # sg.theme('DarkAmber')   # Add a touch of color
  # All the stuff inside your window.

  left_col = [
    [sg.Listbox(pokemon_list, size = (25, 25), enable_events=True, key='-INPUT-')]
  ]

  right_col = [
    [sg.T('Pokemon Details', font='Any 16')],
    [sg.Text('n/a', size = (30, 1), key='-NAME-')],
    [sg.Text('n/a', size = (4, 1), key='-ID-')],
  ]

  layout = [
    [sg.T('Pokemon Selector', font='Any 20')],
    [sg.Column(left_col), sg.Column(right_col)],
    [sg.Button('Close'), sg.Text('https://github.com/AnsonLai/')]
  ]

  # Create the Window
  window = sg.Window('Pokemon Selector', layout)
  # Event Loop to process "events" and get the "values" of the inputs
  prev_input = ""
  while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
          break

      window['-NAME-'].update(values['-INPUT-'][0].upper())
      if (values['-INPUT-'][0].lower() != prev_input):
        prev_input = values['-INPUT-'][0].lower()
        r = requests.get('https://pokeapi.co/api/v2/pokemon/' + values['-INPUT-'][0].lower())
        output = r.json()
        id = output['id']
        window['-ID-'].update(id)

        sprite_url = output['sprites']['front_default']
        img_r = requests.get(sprite_url)
        if img_r.status_code == 200:
          with open(os.path.join(Current_Path, 'sprite.png'), 'wb') as f:
            f.write(img_r.content)

        window['-SPRITE-'].update(os.path.join(Current_Path, 'sprite.png'))


  window.close()

if __name__ == "__main__":
    main()


# pyinstaller -c -F main.py 


*****************************************************************************

  NOTES for Blackjack.exe
        built using py2exe (https://www.py2exe.org/), from
            Blackjack.py
                > gamecards
                    __init__.py
                    cards_people.py
                    standard_cards.py
            by Gary Murdoch

*****************************************************************************

  To play the game:
  
    o double-click on 'Blackjack.exe' in the directory
      'Blackjack Program Files';
    o the program will run in a Windows Command Prompt with your default
      configurations for console size, colours, fonts, etc.
  
  You do not need to be in the 'Blackjack Program Files' directory to
  play the game ... you may find it useful to create a shortcut to the
  executable:
        o right-click on Blackjack.exe
        o select 'Create shortcut' from the drop-down menu
        o a shortcut called 'Blackjack.exe - Shortcut' will appear
        o cut and paste the shortcut to a more convenient location/folder
        o double-click the shortcut, wherever it is, to run the game
        o game transcripts get written to a file called 'all_games.txt'
          inside a folder called 'Games History', within the folder
          'Blackjack Program Files'
              >> 'all_games.txt' is ADDED TO (not overwritten) at the end of
                 every run of Blackjack.exe
              >> if it does not already exist, the file 'all_games.txt' gets
                 created by Blackjack.exe
              >> if a folder called 'Games History' does not already exist
                 inside of 'Blackjack Program Files', then Blackjack.exe
                 will create a 'Games History' folder as well
  
  The game runs in a Windows Command Prompt shell. For a good experience
  including proper rendering of illustrations for the playing cards, set the
  following properties in the DEFAULTS for Command Prompt on your system:
        o Defaults > Font > Size > 20
        o Defaults > Font > Font > Consolas     [ *** THIS IS CRITICAL *** ]
        o Defaults > Layout > Window Size > 120
        o Defaults > Layout > Window Size > Height: 45
        
  You may also need to enable unicode character support on your Windows OS
  generally (in particular to enable the printing of special characters to
  files):
        in WINDOWS 10, navigate to ...
            Control Panel
                > Clock and Region
                    > Region
                        > Administrative
                            > Change system locale
        
        and the TICK THE BOX beside
            "Beta: Use Unicode UTF-8 for worldwide language support"
  
        then RESTART YOUR COMPUTER

  When your computer is running again, double-click on Blackjack.exe
  (or on the shortcut you made earlier) to play.

*****************************************************************************

  For reference, the drawings of playing cards use unicode characters ...
        o character codes for card suits can be found at:
              https://www.w3.org/TR/xml-entity-names/026.html
        o unicodes for card border lines and corners
          (box-drawing and block characters):
              https://www.w3.org/TR/xml-entity-names/025.html

*****************************************************************************
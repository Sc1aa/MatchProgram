# Explanation

Allows user to select two folders of line stimuli and cycle between permutations of stimuli from folder 1 and folder 2 placed on top of each other. Includes option to save and view as gallery.

## Instructions
1. Download MatchProgram Folder
2. On Windows OS, Select: ImageCombiner_WINDOWS.exe
3. Select: MoreInfo >Run-Anyway
4. Click "Select Top Folder" and select folder with top half line stimuli
5. Click "Select Bottom Folder" and select folder with top half line stimuli

IF THE EXECUTE FILE DOES NOT WORK:
- You can run it from the original Python Code located: Code>Combine_Final.py

## Features
Grid View: Displays 3 x 3 Gallery of Permutations 
- Displays info @top + bottom line stimuli currently combined
- WIP: Stored View to view all permutations currently viewed per/Session

Single View: Displays INDIVIDUAL Permutation of Line Stimuli with ability toggle top and bottom stimuli
- Displays info @top + bottom line stimuli currently combined

Save: Saves current viewed as PNG
- WIP: Option to save ALL Stored Permutations @Current Session

## Key Binds
- Left/Right: Toggle Top Stimuli
- Up/Down: Toggle Bottom Stimuli
- Tab: Cycle View
- Enter: Save Current

- Left/Right Arrow: Toggle Between Permutations/Total Stimuli
    - Currently Deprecated (WIP)

# Notes
For whatever reason, running the application from Combine_Final.py out of VSCode directly does dot display visuals on macOS. However, the compiled app, which is using the exact same underlying code, works and displays the stimuli perfectly.

Inorder to make this accessible online, the TKINTER interface would need to be changed.

# Changelog
V1: Combine.py
V1.1: CombineGallery_v0.py
V1.2: CombineGallery_v1.py

V2: Combine_macos.py
V2.1: Combine_Final

Current Experimental Version: Combine_Test.py


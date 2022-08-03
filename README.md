# pataz-anim-toolz
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a simple addon that rearranges some of the animation related UI elements in Blender for more efficient workflow. 
It also comes with a few new tools to help out animators.

## Tools

The addon provides 2 new copy/paste tools:
<img align="right" src="https://user-images.githubusercontent.com/88658022/182589587-592f3666-3839-40b1-b098-eb5449bbdbe8.jpg">

### Copy/paste world coords:
This allows you to copy and paste the absolute position and rotation of objects and bones in world space.
You can copy between objects and bones, and if you have autokey enabled, will set a key as well.
This is handy when switching on and off constraints to ensure that your object or bone maintains its position.

### Copy/paste relative coords:
This copies and pastes the relative position of the active bone to another selected bone, and pastes it back again.
At present it only works between 2 bones, but already this is very useful for when you want to quickly have one bone follow another without setting up a constraint.

For ease of use, right click on these buttons and add them to your Quick Favorites for easy access so that you don't have to keep going back to the panel to use them.
Please note: right now these tools don't work with the ChildOf constraint.

## Settings
<img align="right" src="https://user-images.githubusercontent.com/88658022/182589564-ef5db402-144b-4cea-84ce-05a07d109b34.jpg">

This panel gathers various settings from around Blender's UI into one panel for convenience. 

### Keying
The keying section collects all the keying related settings from Blender's timeline and user prefs for easy access.
It has the autokey button, keying set selection, default new key options and new keying behaviours.

### Playback
The playback section contains the sync mode selector and the start and end frame for the scene or preview range.

### Audio
This is where you can mute the audio and turn scrubbing on and off.

### Optimisation

For now this section only contains simplify, but there are plans to add more settings to this section to optimise viewport performance.

## Bone Selection Sets
<img align="right" src="https://user-images.githubusercontent.com/88658022/182589499-d6837421-18f0-42e3-ac29-5ce0475d5e6e.jpg">

This panel reorganises the UI for the Bone Selection Sets addon that comes with Blender. 
It is only displayed when the active object is an armature in pose mode.
In order to use it, you have to enable the official Bone Selection Sets addon. If the addon is not enabled, a button is displayed so that you can enabled it without having to go to user preferences.
In addition to making use of the official selection sets addon, thus maintaining compatibility, it also changes some of the behaviour.

### Top level buttons:
At the top of the panel are 3 buttons that let you copy, paste or clear all the selection sets.

### Creating a selection set:
By clicking the "New" button you create a new selection set, which you immediately name, and your current selection is assigned to it.

### Selecting:
The behaviour of selecting a set has behaves more like selection in other programs, including most file browsers.
- LMB: selects the bones in that set exclusively; it deselects any other bones not in that set.
- Shift-LMB: adds the set to your selection.
- Ctrl-LMB: removes the set from your selection.

### Selection Set options:
To the right of each set is a button labelled "..." that opens an options panel for that set. It enables you to:
- rename the selection set
- add your selection to that set.
- remove your selection from that set.
- delete the selection set.

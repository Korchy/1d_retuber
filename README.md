# 1D Retuber
Tool for simplifying tubular meshes.

Usage
-
- Switch to Edit mode
- Select some continious edges on tubular mesh
    - Edges should be selected in the longitudinal direction! Traverse selection may cause troubles.
- Press "Start Retube" button
- Scroll mouse wheel
    - +/- ctrl - decrease mesh loops resolution in the perpenducular direction according to selection
    - +/- shift - decrease mesh loops resolution in the parallel direction according to selection
- Press: ESC or ENTER to fix modifications

- two buttons in "Selection only" section only show the perp/parallel selections without modifying mesh geometry

Known issues
-
- may cause troubles when selection is not longtitude
- or if selection lies on the mesh cut

Installation
-
Download the distributive from GitHub

User Preferences - Add-ons - Install Add-on from File - select downloaded archive

Location
-
The 3D_View window - T-panel - the 1D tab - Retuber

Blender version
-
2.79

Developers
-
Paul Kotelevets

Nikita Akimov

Version history
-
1.2.1
- Integrated to the NA 1D Tools

1.2.0
- bug fix

1.1.0
- some improvement
- Esc - esit without mesh modification
- added All selection button - show all selected edges (para + perp)

1.0.0
- first release

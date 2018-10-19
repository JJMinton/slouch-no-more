# slouch-no-more
A python application to detect slouching and alarm user with instructive image to correct their posture.


# Installation and run "interactively":

1. Clone the repository, if not already cloned.
1. Install conda, if not already installed.
1. Create a conda environment with `conda env create -f slouch.yml`.
1. Ensure all the packages are installed correctly and complete with `conda env update -f slouch.yml` after activating the environment. This may require installing other packages (such as cmake and c++) for `dlib` to install correctly.
1. Run `python gui.py`



# TODOs:

1. Solve the need for calibrating the users 'ideal' posture. This is currently required for when the webcam moves so detect background movement, maybe.
1. Run in the background with warning window popping up only when required.

"""This module contains the paths to the
templates that are used in the package. The
templates are stored in the templates folder of
the package.

Attributes:
    - Aero (str): Path to the Aero template. Has a moving gradient background with Quartz theme.
    - Cerulean (str): Path to the Cerulean template.
    - Cosmo (str): Path to the Cosmo template.
    - Cyborg (str): Path to the Cyborg template.
    - Darkly (str): Path to the Darkly template.
    - Default (str): Path to the Default template. Has a built-in theme switcher.
    - Flatly (str): Path to the Flatly template.
    - Journal (str): Path to the Journal template.
    - Litera (str): Path to the Litera template.
    - Lumen (str): Path to the Lumen template.
    - Lux (str): Path to the Lux template.
    - Materia (str): Path to the Materia template.
    - Minty (str): Path to the Minty template.
    - Morph (str): Path to the Morph template.
    - Pulse (str): Path to the Pulse template.
    - Quartz (str): Path to the Quartz template.
    - Sandstone (str): Path to the Sandstone template.
    - Simplex (str): Path to the Simplex template.
    - Sketchy (str): Path to the Sketchy template.
    - Slate (str): Path to the Slate template.
    - Solar (str): Path to the Solar template.
    - Spacelab (str): Path to the Spacelab template.
    - Superhero (str): Path to the Superhero template.
    - United (str): Path to the United template.
    - Vapor (str): Path to the Vapor template.
    - Yeti (str): Path to the Yeti template.
    - Zephyr (str): Path to the Zephyr template.
    - InternalTemplates (class): Internal templates for the package.
"""

from pathlib import Path


Aero = str(Path(__file__).parent.absolute()) + "/aero.html"
Cerulean = str(Path(__file__).parent.absolute()) + "/cerulean.html"
Cosmo = str(Path(__file__).parent.absolute()) + "/cosmo.html"
Cyborg = str(Path(__file__).parent.absolute()) + "/cyborg.html"
Darkly = str(Path(__file__).parent.absolute()) + "/darkly.html"
Default = str(Path(__file__).parent.absolute()) + "/default.html"
Flatly = str(Path(__file__).parent.absolute()) + "/flatly.html"
Journal = str(Path(__file__).parent.absolute()) + "/journal.html"
Litera = str(Path(__file__).parent.absolute()) + "/litera.html"
Lumen = str(Path(__file__).parent.absolute()) + "/lumen.html"
Lux = str(Path(__file__).parent.absolute()) + "/lux.html"
Materia = str(Path(__file__).parent.absolute()) + "/materia.html"
Minty = str(Path(__file__).parent.absolute()) + "/minty.html"
Morph = str(Path(__file__).parent.absolute()) + "/morph.html"
Pulse = str(Path(__file__).parent.absolute()) + "/pulse.html"
Quartz = str(Path(__file__).parent.absolute()) + "/quartz.html"
Sandstone = str(Path(__file__).parent.absolute()) + "/sandstone.html"
Simplex = str(Path(__file__).parent.absolute()) + "/simplex.html"
Sketchy = str(Path(__file__).parent.absolute()) + "/sketchy.html"
Slate = str(Path(__file__).parent.absolute()) + "/slate.html"
Solar = str(Path(__file__).parent.absolute()) + "/solar.html"
Spacelab = str(Path(__file__).parent.absolute()) + "/spacelab.html"
Superhero = str(Path(__file__).parent.absolute()) + "/superhero.html"
United = str(Path(__file__).parent.absolute()) + "/united.html"
Vapor = str(Path(__file__).parent.absolute()) + "/vapor.html"
Yeti = str(Path(__file__).parent.absolute()) + "/yeti.html"
Zephyr = str(Path(__file__).parent.absolute()) + "/zephyr.html"


class InternalTemplates:
    """Internal templates for the package.

    Do not touch these unless you know what you are doing.
    :var - JavaScript: The path to the JavaScript (dynamics.js) file.
    :type - JavaScript: str
    :var - GeneralStyle: The path to the general CSS (general.css) file.
    :type - GeneralStyle: str
    :var - IconSample: The path to the sample icon (doesn't exist anymore) file.
    :type - IconSample: str
    """

    JavaScript = str(Path(__file__).parent.absolute()) + "/Internal/dynamics.js"
    GeneralStyle = str(Path(__file__).parent.absolute()) + "/Internal/general.css"
    IconSample = str(Path(__file__).parent.absolute()) + "/Internal/iconsample.ico"
    ProjectFile = (
        str(Path(__file__).parent.absolute()) + "/Internal/project_template.py"
    )
    TemplatesFolder = str(Path(__file__).parent.absolute())

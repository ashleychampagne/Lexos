from flask import session, render_template, Blueprint, jsonify
from lexos.helpers import constants
from lexos.managers import session_manager
from lexos.models.cutter_model import CutterModel
from lexos.models.filemanager_model import FileManagerModel

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
cutter_blueprint = Blueprint('cutter', __name__)


@cutter_blueprint.route("/cut", methods=["GET"])
def cut():
    """ Handles the functionality of the cut page.

    It cuts the files into various segments depending on the specifications
    chosen by the user, and sends the text segments.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Load the file manager.
    file_manager = FileManagerModel().load_file_manager()

    # Get active file labels with the corresponding id.
    id_label_map = file_manager.get_active_labels_with_id()

    # Get the file preview.
    previews = file_manager.get_previews_of_active()

    # Fill the default cut option into the session.
    if 'cut_option' not in session:
        session['cut_option'] = constants.DEFAULT_CUT_OPTIONS

    return render_template(
        'cut.html',
        itm="cut",
        labels=id_label_map,
        previews=previews)


@cutter_blueprint.route("/downloadCutting", methods=["GET", "POST"])
def download_cutting():
    """downloads cut files.

    :return: a .zip with all the cut files
    """
    # Load the file manager.
    file_manager = FileManagerModel().load_file_manager()

    return file_manager.zip_active_files('cut_files.zip')


@cutter_blueprint.route("/apply_cut", methods=["POST"])
def apply_cut():
    """cuts the files.

    :return: cut files and their preview in a json object
    """
    session_manager.cache_cutting_options()
    return jsonify(
        result=CutterModel().get_cut_files()
    )

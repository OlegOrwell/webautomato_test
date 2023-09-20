from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime


# ---------------------Arguments-------------------------------------
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--source", default="table_A.csv", type=str, help="Name of source file")
parser.add_argument("-t", "--template", default="template.csv", type=str, help="Name of template")
parser.add_argument("-r", "--result", default="result.csv", type=str, help="Name of the file containing results")
args = vars(parser.parse_args())

# ---------------------Directories and Names-------------------------
now = datetime.now().strftime("%H:%M:%S").replace(":", "-")

source_name = args["source"]
source_name = source_name if source_name.endswith('.csv') else source_name + '.csv'

template_name = args["template"]
template_name = template_name if template_name.endswith('.csv') else template_name + '.csv'

result_name = args["result"]
result_name = result_name if result_name.endswith('.csv') else result_name + '.csv'

result_name = result_name.split(".")
result_name = result_name[0] + "_" + now + "." + result_name[1]

ROOT_DIR = "table_transformer"
SOURCES_DIR = "./data/sources/"
TEMPLATES_DIR = "./data/templates/"
RESULTS_DIR = "./data/results/"

directories = {
    "sources_dir": SOURCES_DIR,
    "templates_dir": TEMPLATES_DIR,
    "results_dir": RESULTS_DIR,
}

addresses = {
    "source": SOURCES_DIR + source_name,
    "template": TEMPLATES_DIR + template_name,
    "result": RESULTS_DIR + result_name,
}

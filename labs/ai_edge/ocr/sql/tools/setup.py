import sys, os, argparse

sys.path.append(os.path.split(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0])[0])

from ocr import sql

parser = argparse.ArgumentParser()
parser.add_argument("--connection_string", required=True)
parsed_args = parser.parse_args()

text_admin_db = sql.TextAdmin(parsed_args.connection_string)
text_admin_db.ensure_tables_exist()


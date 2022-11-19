import ibm_db
from src.constants import Dbconstants
dsn = Dbconstants.dsn
conn = ibm_db.connect(dsn, "", "")
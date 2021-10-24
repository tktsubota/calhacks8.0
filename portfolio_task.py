from cs50 import SQL
from models import Student, Transaction

db = SQL("cockroachdb://adam:INszvx_c7RoH_dGI@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/slim-goat-4296.calhacks?sslmode=verify-full&sslrootcert=/Users/adam.manji/Library/CockroachCloud/certs/slim-goat-ca.crt")

def run() :

    users = db.execute("SELECT uid, portfolio_values FROM users")
    for user in users :
        uid = user['uid']
        student = Student(uid)
        port_val = student.evaluate_portfolio(student.get_portfolio())
        port_vals = user['portfolio_values']
        port_vals.append(port_val)
        print(port_val)
        print(port_vals)
        db.execute("UPDATE users SET portfolio_values=ARRAY[:p] WHERE uid=:u", p=port_vals, u=uid)
        try :
            db.execute("COMMIT")
        except :
            pass

run()
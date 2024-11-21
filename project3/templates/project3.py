from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

current_db_details = None

@app.route("/")
def index():
    return render_template("connection.html")

@app.route("/test_connection", methods=["POST"])
def test_connection():
    global current_db_details
    db_details = request.json
    try:
        conn = psycopg2.connect(
            dbname=db_details.get("dbname"),
            user=db_details.get("user"),
            password=db_details.get("password"),
            host=db_details.get("host"),
            port=db_details.get("port")
        )
        conn.close()
        current_db_details = db_details
        return jsonify({"status": "success", "message": "Connection successful"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/management")
def management():
    if not current_db_details:
        return redirect(url_for('index'))
    return render_template("management.html")

@app.route("/load_data", methods=["POST"])
def load_data():
    if not current_db_details:
        return jsonify({"status": "error", "message": "No database connection"})
    
    table_name = request.json.get("table_name")
    try:
        conn = psycopg2.connect(**current_db_details)
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/insert_data", methods=["POST"])
def insert_data():
    if not current_db_details:
        return jsonify({"status": "error", "message": "No database connection"})
    
    data = request.json
    table_name = data.get("table_name")
    student_data = (data.get("masosv"), data.get("hotensv"), data.get("gioitinh"), data.get("lop"))

    try:
        conn = psycopg2.connect(**current_db_details)
        cur = conn.cursor()
        query = sql.SQL(
            "INSERT INTO {} (masosv, hotensv, gioitinh, lop) VALUES (%s, %s, %s, %s)"
        ).format(sql.Identifier(table_name))
        cur.execute(query, student_data)
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Dữ liệu đã được thêm thành công!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/delete_data", methods=["POST"])
def delete_data():
    if not current_db_details:
        return jsonify({"status": "error", "message": "No database connection"})
    
    data = request.json
    table_name = data.get("table_name")
    masosv = data.get("masosv")

    try:
        conn = psycopg2.connect(**current_db_details)
        cur = conn.cursor()
        
        query = sql.SQL("DELETE FROM {} WHERE masosv = %s").format(sql.Identifier(table_name))
        cur.execute(query, (masosv,))

        rows_deleted = cur.rowcount
        
        conn.commit()
        conn.close()
        
        if rows_deleted > 0:
            return jsonify({
                "status": "success", 
                "message": f"Đã xóa sinh viên có mã số {masosv} thành công!",
                "rows_deleted": rows_deleted
            })
        else:
            return jsonify({
                "status": "error", 
                "message": f"Không tìm thấy sinh viên có mã số {masosv}"
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
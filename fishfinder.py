# /// script
# requires-python = ">=3.9"
# ///

import os
import socket
import sqlite3
import traceback
from typing import Dict, List, Tuple

# TODO: dynamic "/" (index.html)
# -- choosing a spot & time
# -- track uncaught fish variants
# -- suggest best spot & time to fish at

# TODO: register fish caught before using the database
# -- spot=None, time=None, stars=3, shiny=true, fish="Mackerel" etc.


AddressPair = Tuple[str, int]  # ("ip_address", port)
Client = Tuple[socket.socket, AddressPair]


def contents_of(filename: str) -> str:
    """get the contents of a UTF-8 text file for caching"""
    with open(filename) as file:
        return file.read()

def spot_and_time_of(route: str) -> Tuple[str, str]:
    return route.split("/")[1:3]


class Server:
    # server
    address: AddressPair
    client: Client
    # database
    db: sqlite3.Connection
    spots: List[str]
    times: List[str]
    # cached assets
    static: Dict[str, Tuple[str, str]]
    # ^ {"route": ("mime/type", "text data")}
    form_html: str
    # properties
    ip: str = property(lambda s: s.address[0])
    port: int = property(lambda s: s.address[1])
    client_socket: socket.socket = property(lambda s: s.client[0])
    client_address: AddressPair = property(lambda s: s.client[1])
    client_ip: str = property(lambda s: s.client[1][0])
    client_port: int = property(lambda s: s.client[1][1])

    def __init__(self, ip: str, port: int):
        self.address = (ip, port)
        self.load_db()
        # quick DB reference
        self.spots = [
            entry[0]
            for entry in self.db.execute(
                "SELECT name FROM Spot").fetchall()]
        self.times = [
            entry[0]
            for entry in self.db.execute(
                "SELECT name FROM Time").fetchall()]
        # static routes
        index_html = contents_of("index.html")
        style_css = contents_of("style.css")
        # TODO: favicon.ico
        self.static = {
            "/": ("text/html", index_html),
            "/index.html": ("text/html", index_html),
            "/style.css": ("text/css", style_css)}
        # dynamic routes
        self.form_html = contents_of("form.html")  # dynamic
        self.client = (None, None)  # placeholder

    def load_db(self):
        self.db = sqlite3.connect(":memory:")
        with open("zzz.fish.base.sql") as base_sql:
            self.db.executescript(base_sql.read())
        with open("zzz.fish.junk.sql") as junk_sql:
            self.db.executescript(junk_sql.read())
        # get catches, if any are saved
        if os.path.exists("catch.history.sql"):
            with open("catch.history.sql") as catches_sql:
                self.db.executescript(catches_sql.read())

    # database queries
    def catches_at(self, spot: str, time: str, limit: int = 5) -> List[List[str]]:
        # NOTE: rowids start at 1, not 0
        spot_rowid = self.spots.index(spot) + 1  # nasty, but w/e
        time_rowid = self.times.index(time) + 1
        query = f"""
            SELECT F.name, C.stars, C.shiny
            FROM Catch as C
            INNER JOIN Fish AS F ON C.fish == F.rowid
            WHERE C.spot == {spot_rowid}
            AND   C.time == {time_rowid}
            ORDER BY C.rowid DESC LIMIT {limit};"""
        return self.db.execute(query).fetchall()

    def fish_at(self, spot: str, time: str) -> List[Tuple[str, str]]:
        # NOTE: rowids start at 1, not 0
        spot_rowid = self.spots.index(spot) + 1  # nasty, but w/e
        time_rowid = self.times.index(time) + 1
        query = f"""
            SELECT F.rowid, F.name
            FROM Fish AS F
            INNER JOIN FishSpot AS FS ON FS.fish == F.rowid
            INNER JOIN FishTime AS FT ON FT.fish == F.rowid
            WHERE FS.spot == {spot_rowid}
            AND   FT.time == {time_rowid};"""
        return self.db.execute(query).fetchall()

    def rates_at(self, spot: str, time: str) -> List[Tuple[str, float]]:
        # NOTE: rowids start at 1, not 0
        spot_rowid = self.spots.index(spot) + 1  # nasty, but w/e
        time_rowid = self.times.index(time) + 1
        # TODO: include 0% catch rate fish
        # -- will likely need the fish_at(spot, time) query
        query = f"""
            SELECT F.name, COUNT(*)
            FROM Catch as C
            INNER JOIN Fish AS F ON C.fish == F.rowid
            WHERE C.spot == {spot_rowid}
            AND   C.time == {time_rowid}
            GROUP BY F.name
            ORDER BY F.rowid;"""
        fish_counts = self.db.execute(query).fetchall()
        total_catches = sum(num_catches for fish, num_catches in fish_counts)
        return [
            (fish, num_catches / total_catches)
            for fish, num_catches in fish_counts]

    # database update
    def log_catch(self, spot, time, fish, stars, shiny: bool):
        shiny = 1 if shiny == "on" else 0
        self.db.execute("""
            INSERT INTO Catch(fish, stars, shiny, spot, time)
            VALUES (?, ?, ?, ?, ?)""",
            (fish, stars, shiny, spot, time))
        catches = self.db.execute("""SELECT * FROM Catch""").fetchall()
        assert len(catches) > 0, "ROW ROW FIGHT THE POWER"
        # update (rebuild) catch.history.sql
        # NOTE: appending to a .csv would be faster
        # -- keeping the whole database in human-readable .sql files is nice tho
        with open("catch.history.sql", "w") as catch_sql:
            catch_sql.write("".join([
                "INSERT INTO Catch VALUES\n",
                ",\n".join([f"    {catch}" for catch in catches]),
                ";"]))
        print("* logged catch")

    def generate_form(self, route: str) -> str:
        spot, time = spot_and_time_of(route)
        # generate html snippets from database queries
        catch_history = ("\n" + " " * 8).join([
            "</td><td>".join([f"<tr><td>{fish}", str(stars), f"{'NY'[shiny]}</td></tr>"])
            for fish, stars, shiny in self.catches_at(spot, time)])
        fish_picker = ("\n" + " " * 8).join([
            f'<option value="{fish_rowid}">{fish}</option>'
            for fish_rowid, fish in self.fish_at(spot, time)])
        catch_rates = ("\n" + " " * 8).join([
            f"<tr><td>{fish}</td><td>{rate * 100:.2f}%</td></tr>"
            for fish, rate in self.rates_at(spot, time)])
        # f"{rate * 100:.2f}%"
        # TODO: css-palette (css vars picked based on time)
        # TODO: player icon location on .svg map of fishing spots
        replacements = {
            "catch-history": catch_history,
            "catch-rates": catch_rates,
            "fish-picker": fish_picker,
            "spot": spot,
            "time": time}
        # replace placeholders with generated html snippets
        form = self.form_html
        for keyword, data in replacements.items():
            placeholder = "{{" + keyword + "}}"
            form = form.replace(placeholder, data)
        return form

    def reply(self):
        """parse & respond to client request"""
        print(f"= connected to {self.client_ip}:{self.client_port}")
        raw_request = self.client_socket.recv(0x8000)
        # parse request
        request = raw_request.decode()
        header, body = request.split("\r\n\r\n")
        header_lines = header.split("\r\n")
        # method line
        method, route, protocol = header_lines[0].split()
        assert protocol == "HTTP/1.1"
        # keyvalues (UNUSED)
        # key_values = dict([
        #     line.split(": ")
        #     for line in lines[0:-1]])
        # respond to request
        if method == "GET":
            self.GET(route)
        elif method == "POST":
            self.POST(route, body)
        else:
            raise NotImplementedError(f"unsupported HTTP method: '{method}'")

    # HTTP methods
    def GET(self, route):
        if route in self.static:
            mime_type, data = self.static[route]
            self.serve_200(mime_type, data)
            print(f"> served static route '{route}'")
        elif route.count("/") == 3:
            if route.endswith("/"):
                self.serve_200("text/html", self.generate_form(route))
                print(f"> served dynamic route '{route}'")
            elif route.endswith("/style.css"):
                # TODO: self.generate_css(route)
                self.serve_200(*self.static["/style.css"])
        else:
            self.serve_404(route)

    def POST(self, route, body):
        # form response -> dict
        form_dict = dict([
            pair.split("=")
            for pair in body.lstrip("/?").split("&")])
        # route decides how we respond
        if route in ("/", "/index.html"):  # redirect to "/Spot/Time/"
            # /?time=T&spot=S
            spot = self.spots[int(form_dict["spot"]) - 1]
            time = self.times[int(form_dict["time"]) - 1]
            new_route = f"/{spot}/{time}/"
            self.serve_303(new_route)
        elif route.count("/") == 3:  # log catch
            # /Spot/Time/?fish=F&stars=S1&shiny=S2&spot=S3&time=T
            spot, time = spot_and_time_of(route)
            spot = self.spots.index(spot) + 1
            time = self.times.index(time) + 1
            form_dict["shiny"] = form_dict.get("shiny", "off")
            self.log_catch(spot, time, **form_dict)
            self.serve_200("text/html", self.generate_form(route))
            print(f"> reloaded dynamic route '{route}'")
        else:
            raise RuntimeError(f"have no response to POST {route} {body}")

    # HTTP responses
    def serve(self, message: List[str]):
        self.client_socket.send("\r\n".join(message).encode())

    def serve_200(self, mime_type: str, data: str):
        """open a file in the browser"""
        self.serve([
            "HTTP/1.1 200 OK",
            f"Content-Type: {mime_type}; charset=UTF-8",
            f"Content-Length: {len(data)}",
            "Connection: close",
            "",
            data])

    def serve_303(self, route: str):
        """redirect to another page"""
        url = f"http://{self.ip}:{self.port}{route}"
        self.serve([
            "HTTP/1.1 303 See Other",
            f"Location: {url}",
            "Content-Type: text/html; charset=UTF-8",
            "Content-Length: 0",
            ""])
        print(f"~ redirected to {route}")

    def serve_404(self, route: str):
        """FileNotFound"""
        # TODO: error page
        self.serve([
            "HTTP/1.1 404 Not Found",
            ""])
        print(f"! file not found '{route}'")

    def serve_500(self):
        """RuntimeError"""
        # TODO: error page
        self.serve([
            "HTTP/1.1 500 Internal Server Error",
            ""])
        print("! server error")

    def serve_501(self):
        """NotImplementedError"""
        # TODO: error page
        self.serve([
            "HTTP/1.1 501 Not Implemented",
            ""])
        print("! not implemented")

    def run(self):
        """main function"""
        # NOTE: syncronous, should only be one user at a time anyway
        with socket.create_server((self.ip, self.port)) as server:
            print(f"@ server is live: http://{self.ip}:{self.port}/")
            while True:
                print("^ listening for a client")
                self.client = server.accept()
                # TODO: respect "Connection: keep-alive"
                # -- need some kind of timeout
                try:
                    self.reply()
                except NotImplementedError:
                    self.serve_501()
                except Exception as exc:
                    self.serve_500()
                    raise exc
                self.client_socket.close()
                print("v connection closed")


if __name__ == "__main__":
    server = Server("0.0.0.0", 8000)
    server.run()

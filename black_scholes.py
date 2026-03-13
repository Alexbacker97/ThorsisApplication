import customtkinter as ctk
from datetime import datetime
import math
import threading
import yfinance as yf


# ══════════════════════════════════════════════════════════════════════════════
#  BLACK-SCHOLES BERECHNUNG
# ══════════════════════════════════════════════════════════════════════════════

def _fehlerfunktion(x):
    """Näherung der Fehlerfunktion (Abramowitz & Stegun)."""
    vorzeichen = 1 if x >= 0 else -1
    x = abs(x)
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return vorzeichen * y

def normalverteilung_cdf(x):
    return 0.5 * (1.0 + _fehlerfunktion(x / math.sqrt(2)))

def black_scholes_berechnung(
    aktienkurs,
    ausuebungspreis,
    laufzeit_jahre,
    risikofreier_zinssatz,
    volatilitaet,
    optionstyp="call"
):
    """
    aktienkurs          – aktueller Kurs der Aktie (S)
    ausuebungspreis     – Strike-Preis der Option (K)
    laufzeit_jahre      – Restlaufzeit in Jahren (T)
    risikofreier_zinssatz – risikofreier Zinssatz als Dezimalzahl (r)
    volatilitaet        – Volatilität als Dezimalzahl (σ)
    optionstyp          – 'call' oder 'put'
    """
    if laufzeit_jahre <= 0:
        if optionstyp == "call":
            return max(aktienkurs - ausuebungspreis, 0), 0, 0, 0, 0, 0
        else:
            return max(ausuebungspreis - aktienkurs, 0), 0, 0, 0, 0, 0

    d1 = (
        math.log(aktienkurs / ausuebungspreis)
        + (risikofreier_zinssatz + 0.5 * volatilitaet ** 2) * laufzeit_jahre
    ) / (volatilitaet * math.sqrt(laufzeit_jahre))
    d2 = d1 - volatilitaet * math.sqrt(laufzeit_jahre)

    abzinsungsfaktor = math.exp(-risikofreier_zinssatz * laufzeit_jahre)

    if optionstyp == "call":
        optionspreis = (
            aktienkurs * normalverteilung_cdf(d1)
            - ausuebungspreis * abzinsungsfaktor * normalverteilung_cdf(d2)
        )
    else:
        optionspreis = (
            ausuebungspreis * abzinsungsfaktor * normalverteilung_cdf(-d2)
            - aktienkurs * normalverteilung_cdf(-d1)
        )

    # ── Greeks ──
    normalverteilung_pdf_d1 = math.exp(-0.5 * d1 ** 2) / math.sqrt(2 * math.pi)

    delta = normalverteilung_cdf(d1) if optionstyp == "call" else normalverteilung_cdf(d1) - 1

    gamma = normalverteilung_pdf_d1 / (
        aktienkurs * volatilitaet * math.sqrt(laufzeit_jahre)
    )

    vega = aktienkurs * math.sqrt(laufzeit_jahre) * normalverteilung_pdf_d1 / 100

    zeitwert_call = (
        -(aktienkurs * volatilitaet * normalverteilung_pdf_d1)
        / (2 * math.sqrt(laufzeit_jahre))
        - risikofreier_zinssatz * ausuebungspreis * abzinsungsfaktor * normalverteilung_cdf(d2)
    ) / 365

    zeitwert_put = (
        -(aktienkurs * volatilitaet * normalverteilung_pdf_d1)
        / (2 * math.sqrt(laufzeit_jahre))
        + risikofreier_zinssatz * ausuebungspreis * abzinsungsfaktor * normalverteilung_cdf(-d2)
    ) / 365

    theta = zeitwert_call if optionstyp == "call" else zeitwert_put

    rho_call = ausuebungspreis * laufzeit_jahre * abzinsungsfaktor * normalverteilung_cdf(d2) / 100
    rho_put  = -ausuebungspreis * laufzeit_jahre * abzinsungsfaktor * normalverteilung_cdf(-d2) / 100
    rho = rho_call if optionstyp == "call" else rho_put

    return optionspreis, delta, gamma, vega, theta, rho


# ══════════════════════════════════════════════════════════════════════════════
#  FARBEN & SCHRIFTEN
# ══════════════════════════════════════════════════════════════════════════════

HINTERGRUNDFARBE    = "#0A0A0A"
KARTENFARBE         = "#111111"
RAHMENFARBE         = "#222222"
AKZENTFARBE         = "#E8E8E8"
GEDAEMPFTE_FARBE    = "#555555"
GRUEN               = "#00C896"
ROT                 = "#FF4757"

SCHRIFT_KLEIN       = ("Courier New", 10)
SCHRIFT_NORMAL      = ("Courier New", 12)
SCHRIFT_GROSS       = ("Courier New", 42, "bold")
SCHRIFT_TITEL       = ("Courier New", 26, "bold")
SCHRIFT_UNTERTITEL  = ("Courier New", 16)
SCHRIFT_BERECHNEN   = ("Courier New", 12, "bold")


# ══════════════════════════════════════════════════════════════════════════════
#  HILFSFUNKTIONEN FÜR WIDGETS
# ══════════════════════════════════════════════════════════════════════════════

def erstelle_beschriftung(elternelement, text):
    """Erstellt ein kleines Abschnittslabel."""
    beschriftung = ctk.CTkLabel(
        elternelement,
        text=text,
        font=SCHRIFT_KLEIN,
        text_color=GEDAEMPFTE_FARBE
    )
    beschriftung.pack(anchor="w", pady=(14, 2))

def erstelle_eingabefeld(elternelement, beschriftungstext, standardwert=""):
    """Erstellt ein beschriftetes Eingabefeld und gibt das Entry-Widget zurück."""
    erstelle_beschriftung(elternelement, beschriftungstext)
    eingabefeld = ctk.CTkEntry(
        elternelement,
        height=38,
        fg_color=KARTENFARBE,
        border_color=RAHMENFARBE,
        border_width=1,
        text_color=AKZENTFARBE,
        font=SCHRIFT_NORMAL,
        placeholder_text_color=GEDAEMPFTE_FARBE
    )
    eingabefeld.insert(0, standardwert)
    eingabefeld.pack(fill="x")
    return eingabefeld

def erstelle_marktkarte(elternelement, beschriftungstext):
    """Erstellt eine kleine Karte für Marktdaten und gibt das Wert-Label zurück."""
    karte = ctk.CTkFrame(
        elternelement,
        fg_color=KARTENFARBE,
        corner_radius=6
    )
    karte.pack(side="left", fill="x", expand=True, padx=(0, 8))

    ctk.CTkLabel(
        karte,
        text=beschriftungstext,
        font=SCHRIFT_KLEIN,
        text_color=GEDAEMPFTE_FARBE
    ).pack(anchor="w", padx=16, pady=(12, 2))

    wert_label = ctk.CTkLabel(
        karte,
        text="—",
        font=SCHRIFT_NORMAL,
        text_color=AKZENTFARBE
    )
    wert_label.pack(anchor="w", padx=16, pady=(0, 12))
    return wert_label


# ══════════════════════════════════════════════════════════════════════════════
#  HAUPTFENSTER
# ══════════════════════════════════════════════════════════════════════════════

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

hauptfenster = ctk.CTk()
hauptfenster.title("BLACK-SCHOLES  /  OPTIONS PRICER")
hauptfenster.geometry("1100x740")
hauptfenster.configure(fg_color=HINTERGRUNDFARBE)
hauptfenster.resizable(False, False)


# ── Kopfzeile ────────────────────────────────────────────────────────────────

kopfzeile = ctk.CTkFrame(hauptfenster, fg_color=HINTERGRUNDFARBE, height=60)
kopfzeile.pack(fill="x", padx=30, pady=(20, 0))

ctk.CTkLabel(
    kopfzeile,
    text="BLACK-SCHOLES",
    font=SCHRIFT_TITEL,
    text_color=AKZENTFARBE
).pack(side="left")

ctk.CTkLabel(
    kopfzeile,
    text="/ OPTIONS PRICER",
    font=SCHRIFT_UNTERTITEL,
    text_color=GEDAEMPFTE_FARBE
).pack(side="left", padx=(8, 0))

zeitstempel_label = ctk.CTkLabel(
    kopfzeile,
    text=datetime.now().strftime("%Y-%m-%d  %H:%M"),
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE
)
zeitstempel_label.pack(side="right")

ctk.CTkFrame(
    hauptfenster,
    height=1,
    fg_color=RAHMENFARBE
).pack(fill="x", padx=30, pady=(10, 0))


# ── Hauptbereich ─────────────────────────────────────────────────────────────

hauptbereich = ctk.CTkFrame(hauptfenster, fg_color=HINTERGRUNDFARBE)
hauptbereich.pack(fill="both", expand=True, padx=30, pady=20)

linke_spalte = ctk.CTkFrame(hauptbereich, fg_color=HINTERGRUNDFARBE, width=340)
linke_spalte.pack(side="left", fill="y")
linke_spalte.pack_propagate(False)

rechte_spalte = ctk.CTkFrame(hauptbereich, fg_color=HINTERGRUNDFARBE)
rechte_spalte.pack(side="left", fill="both", expand=True, padx=(20, 0))


# ── Linke Spalte: Eingaben ────────────────────────────────────────────────────

# Ticker-Eingabe mit Fetch-Button
erstelle_beschriftung(linke_spalte, "TICKER-SYMBOL")

ticker_zeile = ctk.CTkFrame(linke_spalte, fg_color=HINTERGRUNDFARBE)
ticker_zeile.pack(fill="x")

ticker_eingabe = ctk.CTkEntry(
    ticker_zeile,
    height=38,
    fg_color=KARTENFARBE,
    border_color=RAHMENFARBE,
    border_width=1,
    text_color=AKZENTFARBE,
    font=SCHRIFT_NORMAL,
    placeholder_text="z.B. AAPL",
    placeholder_text_color=GEDAEMPFTE_FARBE
)
ticker_eingabe.pack(side="left", fill="x", expand=True)

abrufen_button = ctk.CTkButton(
    ticker_zeile,
    text="ABRUFEN",
    width=80,
    height=38,
    fg_color=RAHMENFARBE,
    hover_color="#333333",
    text_color=AKZENTFARBE,
    font=SCHRIFT_KLEIN,
    corner_radius=4
)
abrufen_button.pack(side="left", padx=(6, 0))

# Weitere Eingabefelder
ausuebungspreis_eingabe = erstelle_eingabefeld(linke_spalte, "AUSÜBUNGSPREIS (K)", "")
ablaufdatum_eingabe     = erstelle_eingabefeld(linke_spalte, "ABLAUFDATUM (JJJJ-MM-TT)", "")
zinssatz_eingabe        = erstelle_eingabefeld(linke_spalte, "RISIKOFREIER ZINSSATZ (%)", "4.5")
volatilitaet_eingabe    = erstelle_eingabefeld(linke_spalte, "VOLATILITÄT (%) — ÜBERSCHREIBEN", "")

# Optionstyp-Auswahl
erstelle_beschriftung(linke_spalte, "OPTIONSTYP")

optionstyp_variable = ctk.StringVar(value="call")

optionstyp_zeile = ctk.CTkFrame(linke_spalte, fg_color=HINTERGRUNDFARBE)
optionstyp_zeile.pack(fill="x")

call_button = ctk.CTkButton(
    optionstyp_zeile,
    text="CALL",
    height=34,
    width=120,
    fg_color=GRUEN,
    hover_color="#00a07a",
    text_color=HINTERGRUNDFARBE,
    font=SCHRIFT_KLEIN,
    corner_radius=4
)
put_button = ctk.CTkButton(
    optionstyp_zeile,
    text="PUT",
    height=34,
    width=120,
    fg_color=KARTENFARBE,
    hover_color="#222222",
    text_color=GEDAEMPFTE_FARBE,
    font=SCHRIFT_KLEIN,
    corner_radius=4
)
call_button.pack(side="left")
put_button.pack(side="left", padx=(6, 0))

def call_auswaehlen():
    optionstyp_variable.set("call")
    call_button.configure(fg_color=GRUEN, text_color=HINTERGRUNDFARBE, hover_color="#00a07a")
    put_button.configure(fg_color=KARTENFARBE, text_color=GEDAEMPFTE_FARBE, hover_color="#222222")

def put_auswaehlen():
    optionstyp_variable.set("put")
    put_button.configure(fg_color=ROT, text_color=HINTERGRUNDFARBE, hover_color="#cc3a47")
    call_button.configure(fg_color=KARTENFARBE, text_color=GEDAEMPFTE_FARBE, hover_color="#222222")

call_button.configure(command=call_auswaehlen)
put_button.configure(command=put_auswaehlen)

# Berechnen-Button
berechnen_button = ctk.CTkButton(
    linke_spalte,
    text="BERECHNEN",
    height=44,
    fg_color=AKZENTFARBE,
    hover_color="#cccccc",
    text_color=HINTERGRUNDFARBE,
    font=SCHRIFT_BERECHNEN,
    corner_radius=4
)
berechnen_button.pack(fill="x", pady=(20, 0))

# Statusmeldung
status_meldung = ctk.CTkLabel(
    linke_spalte,
    text="",
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE,
    wraplength=320,
    justify="left"
)
status_meldung.pack(anchor="w", pady=(8, 0))


# ── Rechte Spalte: Ergebnisse ─────────────────────────────────────────────────

# Großes Preis-Display
preis_karte = ctk.CTkFrame(rechte_spalte, fg_color=KARTENFARBE, corner_radius=6)
preis_karte.pack(fill="x", pady=(0, 12))

preis_innenbereich = ctk.CTkFrame(preis_karte, fg_color=KARTENFARBE)
preis_innenbereich.pack(padx=24, pady=18)

ctk.CTkLabel(
    preis_innenbereich,
    text="THEORETISCHER OPTIONSPREIS",
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE
).pack(anchor="w")

optionspreis_anzeige = ctk.CTkLabel(
    preis_innenbereich,
    text="—",
    font=SCHRIFT_GROSS,
    text_color=AKZENTFARBE
)
optionspreis_anzeige.pack(anchor="w")

# Marktdaten-Zeile
marktdaten_zeile = ctk.CTkFrame(rechte_spalte, fg_color=HINTERGRUNDFARBE)
marktdaten_zeile.pack(fill="x", pady=(0, 12))

kassakurs_wert    = erstelle_marktkarte(marktdaten_zeile, "KASSAKURS")
volatilitaet_wert = erstelle_marktkarte(marktdaten_zeile, "HIST. VOLATILITÄT")
restlaufzeit_wert = erstelle_marktkarte(marktdaten_zeile, "RESTLAUFZEIT")

# Greeks-Anzeige
ctk.CTkLabel(
    rechte_spalte,
    text="GRIECHEN (GREEKS)",
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE
).pack(anchor="w", pady=(4, 6))

greeks_zeile = ctk.CTkFrame(rechte_spalte, fg_color=HINTERGRUNDFARBE)
greeks_zeile.pack(fill="x")

greek_anzeigewerte = {}
for greek_name in ["DELTA", "GAMMA", "VEGA", "THETA", "RHO"]:
    greek_karte = ctk.CTkFrame(greeks_zeile, fg_color=KARTENFARBE, corner_radius=6)
    greek_karte.pack(side="left", fill="x", expand=True, padx=(0, 8))

    ctk.CTkLabel(
        greek_karte,
        text=greek_name,
        font=SCHRIFT_KLEIN,
        text_color=GEDAEMPFTE_FARBE
    ).pack(anchor="w", padx=14, pady=(10, 2))

    greek_wert = ctk.CTkLabel(
        greek_karte,
        text="—",
        font=SCHRIFT_NORMAL,
        text_color=AKZENTFARBE
    )
    greek_wert.pack(anchor="w", padx=14, pady=(0, 10))
    greek_anzeigewerte[greek_name] = greek_wert

# Parameter-Zusammenfassung
ctk.CTkLabel(
    rechte_spalte,
    text="EINGABEPARAMETER",
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE
).pack(anchor="w", pady=(16, 6))

parameter_karte = ctk.CTkFrame(rechte_spalte, fg_color=KARTENFARBE, corner_radius=6)
parameter_karte.pack(fill="x")

parameter_anzeige = ctk.CTkLabel(
    parameter_karte,
    text="—",
    font=SCHRIFT_KLEIN,
    text_color=GEDAEMPFTE_FARBE,
    justify="left",
    anchor="w"
)
parameter_anzeige.pack(anchor="w", padx=18, pady=14)


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIK: DATEN ABRUFEN & BERECHNEN
# ══════════════════════════════════════════════════════════════════════════════

abgerufene_daten = {}

def zeige_status(nachricht, farbe=GEDAEMPFTE_FARBE):
    status_meldung.configure(text=nachricht, text_color=farbe)

def daten_abrufen():
    ticker_symbol = ticker_eingabe.get().strip().upper()
    if not ticker_symbol:
        zeige_status("Bitte ein Ticker-Symbol eingeben.", ROT)
        return

    zeige_status(f"Lade {ticker_symbol} …")
    abrufen_button.configure(state="disabled")

    def _hintergrund_abruf():
        try:
            aktie = yf.Ticker(ticker_symbol)
            marktinfo = aktie.fast_info
            kursverlauf = aktie.history(period="1y")

            if kursverlauf.empty:
                hauptfenster.after(0, lambda: zeige_status("Keine Daten für dieses Symbol.", ROT))
                return

            kassakurs = marktinfo.last_price
            schlusskurse = kursverlauf["Close"]

            log_renditen = [
                math.log(schlusskurse.iloc[i] / schlusskurse.iloc[i - 1])
                for i in range(1, len(schlusskurse))
            ]
            durchschnitt = sum(log_renditen) / len(log_renditen)
            varianz = sum((r - durchschnitt) ** 2 for r in log_renditen) / len(log_renditen)
            historische_volatilitaet = math.sqrt(varianz) * math.sqrt(252)

            abgerufene_daten["kassakurs"]  = kassakurs
            abgerufene_daten["volatilitaet"] = historische_volatilitaet
            abgerufene_daten["ticker"]     = ticker_symbol

            def _oberflaeche_aktualisieren():
                kassakurs_wert.configure(text=f"${kassakurs:.2f}")
                volatilitaet_wert.configure(text=f"{historische_volatilitaet * 100:.1f}%")
                if not volatilitaet_eingabe.get().strip():
                    volatilitaet_eingabe.delete(0, "end")
                    volatilitaet_eingabe.insert(0, f"{historische_volatilitaet * 100:.2f}")
                zeige_status(f"✓ {ticker_symbol} erfolgreich geladen.", GRUEN)
                abrufen_button.configure(state="normal")

            hauptfenster.after(0, _oberflaeche_aktualisieren)

        except Exception as fehler:
            hauptfenster.after(0, lambda: zeige_status(f"Fehler: {fehler}", ROT))
            hauptfenster.after(0, lambda: abrufen_button.configure(state="normal"))

    threading.Thread(target=_hintergrund_abruf, daemon=True).start()


def berechnung_durchfuehren():
    try:
        kassakurs = abgerufene_daten.get("kassakurs")
        volatilitaet = abgerufene_daten.get("volatilitaet")

        if not kassakurs:
            zeige_status("Bitte zuerst Ticker-Daten abrufen.", ROT)
            return

        ausuebungspreis = float(ausuebungspreis_eingabe.get().strip())
        ablaufdatum     = datetime.strptime(ablaufdatum_eingabe.get().strip(), "%Y-%m-%d")
        laufzeit_jahre  = max((ablaufdatum - datetime.now()).days / 365, 0)
        zinssatz        = float(zinssatz_eingabe.get().strip()) / 100

        vol_ueberschreiben = volatilitaet_eingabe.get().strip()
        if vol_ueberschreiben:
            volatilitaet = float(vol_ueberschreiben) / 100

        gewaehlter_optionstyp = optionstyp_variable.get()

        ergebnis = black_scholes_berechnung(
            aktienkurs=kassakurs,
            ausuebungspreis=ausuebungspreis,
            laufzeit_jahre=laufzeit_jahre,
            risikofreier_zinssatz=zinssatz,
            volatilitaet=volatilitaet,
            optionstyp=gewaehlter_optionstyp
        )
        berechneter_preis, delta, gamma, vega, theta, rho = ergebnis

        anzeigefarbe = GRUEN if gewaehlter_optionstyp == "call" else ROT
        optionspreis_anzeige.configure(
            text=f"${berechneter_preis:.4f}",
            text_color=anzeigefarbe
        )

        kassakurs_wert.configure(text=f"${kassakurs:.2f}")
        volatilitaet_wert.configure(text=f"{volatilitaet * 100:.1f}%")
        restlaufzeit_wert.configure(text=f"{laufzeit_jahre * 365:.0f} Tage")

        greek_anzeigewerte["DELTA"].configure(text=f"{delta:+.4f}")
        greek_anzeigewerte["GAMMA"].configure(text=f"{gamma:.5f}")
        greek_anzeigewerte["VEGA"].configure(text=f"{vega:.4f}")
        greek_anzeigewerte["THETA"].configure(text=f"{theta:+.4f}")
        greek_anzeigewerte["RHO"].configure(text=f"{rho:+.4f}")

        parameter_anzeige.configure(
            text=(
                f"S = ${kassakurs:.2f}   "
                f"K = ${ausuebungspreis:.2f}   "
                f"T = {laufzeit_jahre:.4f} Jahre   "
                f"r = {zinssatz * 100:.2f}%   "
                f"σ = {volatilitaet * 100:.2f}%   "
                f"Typ = {gewaehlter_optionstyp.upper()}"
            )
        )

        zeige_status("Berechnung abgeschlossen.", GRUEN)

    except ValueError as wertfehler:
        zeige_status(f"Eingabefehler: {wertfehler}", ROT)
    except Exception as fehler:
        zeige_status(f"Fehler: {fehler}", ROT)


abrufen_button.configure(command=daten_abrufen)
berechnen_button.configure(command=berechnung_durchfuehren)


# ══════════════════════════════════════════════════════════════════════════════
#  STARTEN
# ══════════════════════════════════════════════════════════════════════════════

hauptfenster.mainloop()

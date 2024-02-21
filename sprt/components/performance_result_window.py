import csv
from tkinter import BOTH, VERTICAL, X, filedialog, messagebox, ttk

from sprt.analysis.time_measure import PerformanceResultsData
from sprt.components import ScrollableFrame
from sprt.components.charts.performance import (
    AlgorithmTimePerTextSetChart,
    TextSetPerAlgorithmTimeChart,
)
from sprt.logger import logger

from .active_label import ActiveLabel
from .top_level_abc import TopLevelABC


class PerformanceResultWindow(TopLevelABC):
    def __init__(self, measurement_results: PerformanceResultsData):
        super().__init__(title="Analiza czasu działania", width=1200, height=800)
        self.measurements = measurement_results

        scroll = ScrollableFrame(self, VERTICAL)
        scroll.pack(expand=True, fill=BOTH)
        frame = scroll.inner_frame

        ActiveLabel(
            frame,
            text="Analiza wydajności wybranych algorytmów pod względem działania na wybranych zbiorach.",
            padding=5,
        ).pack(fill=X, ipadx=5)

        ttk.Button(
            frame, text="Eksportuj dane pomiarowe", command=self.__dump_to_csv, padding=5
        ).pack(expand=True, fill=X)

        for algorithm, results in measurement_results.data.items():
            AlgorithmTimePerTextSetChart(
                frame,
                algorithm,
                patterns=measurement_results.patterns_length,
                text_sets_result=results,
            ).pack(fill=X, pady=5)

        for text_set_name, results in measurement_results.transformed_data.items():
            TextSetPerAlgorithmTimeChart(
                frame, text_set_name, measurement_results.patterns_length, results
            ).pack(fill=X, pady=5)

    def __dump_to_csv(self):
        """
        pattern_length, algorithm, text_set, time, deviation
        """
        logger.info("Dump time measurements to CSV initiated")
        file = filedialog.asksaveasfile(
            title="Wybierz miejsce do zapisu", filetypes=[("csv", ".csv")]
        )
        if not file:
            return

        dump = csv.writer(file, dialect="excel")
        dump.writerow(["dlugość_wzorca", "algorytm", "nazwa_zbioru", "średni_czas", "dewiacja"])

        for alg_name, text_set_measurements in self.measurements.data.items():
            for text_set_name, measurements in text_set_measurements.items():
                for pattern_len, time, dev in zip(
                    self.measurements.patterns_length, measurements.time, measurements.stdev
                ):
                    dump.writerow([pattern_len, alg_name, text_set_name, time, dev])

        logger.info("Dump time measurements to CSV succeeded")
        messagebox.showinfo("Sukces", "Plik został zapisany!")

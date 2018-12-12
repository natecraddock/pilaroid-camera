import subprocess
import time
import os
import img2pdf


class Printer:
    def __init__(self):
        pass

    def print_image(self, image):
        # Convert to PDF for nicer printing
        pdf = self._to_pdf(image, "print")
        # Turn off display while printing
        # subprocess.call("./off.sh", shell=True)
        subprocess.run(["lp", "-d", "thermal_printer", "-o", "fit-to-page", pdf])
        # time.sleep(20)
        # print("Finished Printing")
        # subprocess.call("./on.sh", shell=True)

    def _to_pdf(self, image, name):
        with open(name + '.pdf', "wb") as f:
            f.write(img2pdf.convert(image))

        return name + '.pdf'

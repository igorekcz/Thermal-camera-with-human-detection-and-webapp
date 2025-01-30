import numpy as np
from PIL import Image
import io

class Frame:
    def __init__(self, frameID, frame_width, frame_height, tempThreshold, tempMax, humanAreaMin, tempValues) -> None:
        self.frameID = frameID
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.tempThreshold = tempThreshold
        self.tempMax = tempMax
        self.humanAreaMin = humanAreaMin
        self.tempValues = tempValues
        self.regionBitmaps = []
        self.finalFrame = []

        self.process_frame()

    def process_frame(self):
        """
        Process the frame by applying color transformations and identifying regions.

        This method takes the temperature values from the `tempValues` attribute and performs the following steps:
        1. Calculates the minimum and maximum temperature values.
        2. Maps the temperature values to a grayscale color range.
        3. Identifies regions based on temperature thresholds.
        4. Stores the regions in the `regionBitmaps` attribute.
        5. Modifies the colors of the regions based on their index.

        Returns:
            None
        """
        colors = []
        markedFrame = []
        color_v = self.tempValues
        min_temp = min(color_v)
        max_temp = max(color_v)
        m = 255 / max_temp
        d = m * min_temp
        for temp in color_v:
            val = int(m * temp - d)
            colors.append((val, val, val))
            if temp <= self.tempThreshold or temp >= self.tempMax:
                markedFrame.append(0)
            else:
                markedFrame.append(1)

        direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i in range(len(markedFrame)):
            if markedFrame[i] == 1:
                stack = [i]
                markedFrame[i] = 0
                region = [0] * len(colors)
                region[i] = 1
                areaSize = 1
                while stack:
                    index = stack.pop()
                    for d in direction:
                        x, y = index % self.frame_width + d[1], index // self.frame_width + d[0]
                        if 0 <= x < self.frame_width and 0 <= y < self.frame_height:
                            if markedFrame[y * self.frame_width + x] == 1:
                                stack.append(y * self.frame_width + x)
                                region[y * self.frame_width + x] = 1
                                markedFrame[y * self.frame_width + x] = 0
                                areaSize += 1
                if areaSize >= self.humanAreaMin:
                    self.regionBitmaps.append(region)

        if len(self.regionBitmaps) == 0:
            self.finalFrame = colors
            return

        for n, reg in enumerate(self.regionBitmaps):
            for i in range(len(self.tempValues)):
                if reg[i] == 0 and n == 0:
                    self.finalFrame.append(colors[i])
                elif reg[i] == 0:
                    continue
                else:
                    color = colors[i]
                    if n == 0:
                        self.finalFrame.append((int(color[0]/2), color[1], int(color[2]/2)))
                    elif n % 3 == 0:
                        self.finalFrame[i] =(int(color[0]/2), color[1], int(color[2]/2))
                    elif n % 3 == 1:
                        self.finalFrame[i] =(color[0], int(color[1]/2), int(color[2]/2))
                    else:
                        self.finalFrame[i] =(int(color[0]/2), int(color[1]/2), color[2])
        return
    
    def getMaxTemps(self):
        """
        Returns the maximum temperature of each human region in the frame.

        Returns:
          list: The maximum temperature of each human region in the frame.
        """
        maxTemps = []
        for region in self.regionBitmaps:
            maxTemp = max([self.tempValues[i] for i in range(len(region)) if region[i] == 1])
            maxTemps.append(maxTemp)
        return maxTemps
    
    def __str__(self) -> str:
        """
        Prints the result of the current frame.
        """
        maxTemps = self.getMaxTemps()
        if maxTemps != []:
            return f"Detected {len(self.regionBitmaps)} human(s) with max temperatures {maxTemps} in frame {self.frameID}"
        else:
            return f"No human detected in frame {self.frameID}"
        
    def getJpeg(self, scale=20):
        """
        Returns the frame as a JPEG image.

        Returns:
          PIL.Image: The frame as a JPEG image.
        """
        array = np.array(self.finalFrame, dtype=np.uint8).reshape(self.frame_height, self.frame_width, 3)
        img = Image.fromarray(array, "RGB")
        img = img.resize((self.frame_width * scale, self.frame_height * scale), Image.NEAREST)
        with io.BytesIO() as output:
            img.save(output, format="JPEG")
            jpeg_data = output.getvalue()
        return jpeg_data
    
    def getAvgTemp(self):
        return round(sum(self.tempValues) / len(self.tempValues), 1)
    
if __name__ == "__main__":
    with open("Materiał/H100_F250_16HZ_Normalny3.txt") as f:
      color_v = []
      i = 0
      for line in f:
        for temp in line.strip().split():
            color_v.append(float(temp))
        if len(color_v) % (24 * 32) == 0:
            frame = Frame(i, 32, 24, 23, 38, 80, color_v)
            i += 1
            print(frame)
            color_v = []

  

            
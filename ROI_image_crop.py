import cv2

class staticROI(object):

    def __init__(self):

        self.capture = cv2.VideoCapture(0)

        # Uzimanje koordinata bounding box-a
        while True:
            
            self.image_coordinates = []
            self.extract = False
            self.selected_ROI = False

            self.update()

    def update(self):

        while True:

            if self.capture.isOpened():
                # Citanje frejma
                (self.status, self.frame) = self.capture.read()
                
                cv2.imshow('image', self.frame)
                key = cv2.waitKey(2)

                # Kropovanje slike
                if key == ord('c'):

                    self.clone = self.frame.copy()
                    
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)

                    while True:

                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)

                        # Kropovanje i prikaz isecene slike
                        if key == ord('c'):

                            self.crop_ROI()
                            self.show_cropped_ROI()

                        # Nastavak stream-a
                        if key == ord('r'):

                            break
                # Gasenje programa tasterom 'q'
                if key == ord('q'):

                    cv2.destroyAllWindows()
                    exit(1)
            else:
                pass

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Levim klikom osluskuju se koordinate (x1, y1)
        if event == cv2.EVENT_LBUTTONDOWN:

            self.image_coordinates = [(x,y)]
            self.extract = True

        # Pustanjem levog klika se osluskuju koordinate (x2, y2)
        elif event == cv2.EVENT_LBUTTONUP:

            self.image_coordinates.append((x,y))
            self.extract = False

            self.selected_ROI = True

            # Crtanje ROI-a
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)

        # Ciscenje linija desnim klikom
        elif event == cv2.EVENT_RBUTTONDOWN:

            self.clone = self.frame.copy()
            self.selected_ROI = False

    def crop_ROI(self):

        if self.selected_ROI:

            self.cropped_image = self.frame.copy()

            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]

            self.cropped_image = self.cropped_image[y1:y2, x1:x2]

            print('Cropped image: {} {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
        
        else:

            print('Select ROI')

    def show_cropped_ROI(self):

        cv2.imshow('Cropped image', self.cropped_image)

if __name__ == '__main__':

    static_ROI = staticROI()
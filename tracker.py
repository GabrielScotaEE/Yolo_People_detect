import math
from itertools import chain

class EuclideanDistTracker:
    def __init__(self, maxDisappeared=35):
        # Store the center positions of the objects
        self.center_points = {}
        self.disappeared = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.maxDisappeared = maxDisappeared

    
    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + w) // 2
            cy = (y + h) // 2
            

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 18:
                    self.center_points[id] = (cx, cy)
                    self.disappeared[id] = 0
                    #print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                self.disappeared[self.id_count] = 0
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
        cleaner_list = [] 
         

        # Clean the dictionary by center points to remove IDS not used anymore
        self.current_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            self.current_center_points[object_id] = center

        # Comparing last frame with the current frame ids
        for ids, wt in self.center_points.items():
            sucess = self.current_center_points.get(ids)
            if sucess is None:
                self.disappeared[ids] = self.disappeared[ids] + 1
                if self.disappeared[ids] > self.maxDisappeared:
                    cleaner_list.append(ids)
        # Search for repeated centers in center_points
        flipped = {}
        # this for returns exemple: final_dictionary {(20, 30): [1, 11, 15], (25, 17): [5], (50, 40): [7, 10]}
        for key, value in self.center_points.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                flipped[value].append(key)
        # We just need dict.values() > 1
        for repeated in flipped.values():
            if len(repeated)>1:
                repeated.pop(-1)
                for sep in repeated:
                    cleaner_list.append(sep)
  

        
        for clean in cleaner_list:
            del self.disappeared[clean]
            del self.center_points[clean]
            

        # Update dictionary with IDs not used removed
        #self.center_points = self.current_center_points.copy()
        
        return objects_bbs_ids


# test = EuclideanDistTracker()
# test.update([[52, 304, 79, 415], [190, 30, 204, 88], [314, 12, 334, 70]])
# #print(test.center_points)
# print(test.current_center_points)
# test.update([[52, 304, 79, 415], [190, 30, 204, 88]])
# #print(test.center_points)
# print(test.current_center_points)

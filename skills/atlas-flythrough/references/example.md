# Example run: a flythrough of a potter's studio

The request was "make a flythrough of this studio", from one 16:9 image of a potter's studio seen
from its doorway: a work table with a wheel and unfired bowls in the middle of the room, shelves
of pots along the walls, a kiln in a corner, windows on the left. No route was named, and none
was chosen until the scene had been built.

These are the choices made for this scene. Another scene, or another reading of the request,
calls for different ones. The run used the CLI alone, with contact sheets at the check-ins.

## What posing returned

[`pose-request.json`](../assets/example/pose-request.json) is the request and
[`pose-result.json`](../assets/example/pose-result.json) the part of the saved result that
matters. The camera is 0.97 above the floor and tilted about 7 degrees down. `fx` is 762 on a
1280-wide grid, an 80 degree horizontal field of view.

Reading the depth file gave a typical (median) depth of 2.5. The door frame is 1.3 from the
camera, so the camera stands outside the room. Beyond the frame the room is about 4 wide and 4.4
deep. The work table sits just inside the door with open floor on both sides and behind it. The
image says nothing about the wall the door is in, or about what is behind the camera.

## Building the scene

Three rounds. Each is one request with depth, with every frame kept so far as context.

**Round 1: step into the room.** Three cameras on floor the photo showed as open, each looking
where the photo did not: left of the table looking across it at the right wall, right of the
table looking across it at the window wall, and behind the table looking into the back corner.
Each saw about half known surface. What came back: the shelves run the whole right wall to the
door, windows run the whole left wall, and the kiln and back corner are now seen from close up.

**Round 2: the far end, looking back.** Nothing so far showed the wall with the door in it. Three
cameras at the back of the room, in floor that round 1 had confirmed as open, looking back
toward the door from the middle, the left and the right. What came back: through the doorway
there is a large workshop hall with an open dark ceiling, strip lights and rows of shelving. The
model invented all of it, and views 4 and 5 agree on it.

View 6 did not agree. It showed the window wall running on past the door into the hall, where
view 4 shows a wall with shelves, and a grey exit door nobody else had seen. It was kept at
first. A round and a path built on it carried the exit door and the missing wall into the last
two seconds of the video, which is what exposed it. View 6 was dropped, and round 3 and the path
were generated again without it. A view that disagrees is cheapest to drop when it arrives.

**Round 3: what round 2 left thin.** Four cameras: beside the table on each side, looking at the
corners either side of the door; near the back, looking at the door's left side from a spot that
overlaps view 4 (it saw 82% known surface, where view 6's camera had seen 27%); and beside the
source camera, for a second look at the door frame, which only the source image had seen.

[`round-2-request.json`](../assets/example/round-2-request.json) is a whole round's request: the
four frames so far as context, three cameras, and `"returnDepth": true`.
[`round-1-request.json`](../assets/example/round-1-request.json) and
[`round-3-request.json`](../assets/example/round-3-request.json) are the others. The rounds took
18, 30 and 26 seconds and cost 70, 70 and 80 credits.

[`views.jpg`](../assets/example/views.jpg) shows the source image and all ten views by round.
The table, wheel, bowls, kiln and shelves keep their shape and place throughout.

## What the person saw

The contact sheet, with three notes: everything through the doorway is invented; the floor
changes from dusty concrete to smooth grey at the door; and the corner to the left of the door is
the least settled part of the scene. Then the cost and time of the video, about 1,570 credits
and two minutes. They agreed to continue.

## The path

The shot was chosen from the scene. Its best moment, looking back across the table and out
through the door into the hall, did not exist in the photo.

- 8 seconds at 24 frames a second: 192 cameras.
- The first camera is the posed source camera, so the video opens on the photo.
- It goes in through the door to the left of the table, along the window wall to the back of the
  room, round behind the table past the kiln, and forward along the right side. It turns as it
  goes and ends looking over the table and out through the doorway.
- It is seven positions with a point to look at from each. The 192 cameras are read off a smooth
  curve through them, easing in and out. The route is 7.4 long; the largest step between frames
  is 0.046 and the largest turn 2.8 degrees.
- It ends on the doorway and keeps the unsettled corner out of the frame.

Checked against the scene before sending, every camera stood in open space and saw at least 84%
known surface. Against the source image alone, the second half of the same path would have seen
between 20% and 47%: the model would have been inventing the room as the camera turned.

[`path-request.json`](../assets/example/path-request.json) is the request with 9 of the 192
target cameras kept (every 24th and the last) so the file stays small. Its context is the posed
frame and the nine views that were kept, each with its depth.

## The result

One request, 114 seconds, 192 JPEG frames at 1280x720, 1,568 credits.
[`frames.jpg`](../assets/example/frames.jpg) shows twelve of them in order.

- The first frame matches the photo.
- The table, wheel, kiln and shelves hold their shape all the way round the room.
- Looking back, the doorway and the hall beyond it match what views 4, 5, 7 and 8 showed.
- In the last second the window wall and the hall's windows read as one long row, with no clear
  break where the door wall should be. One more view of that corner would have settled it.

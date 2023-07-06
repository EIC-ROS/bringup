test lift_controller package

1. go to workspace
    $ catkin build

2. run ros master
    $ roscore

3. run lift server
    $ rosrun lift_controller lift_controller_node.py

4. run lift client
    $ rosrun lift_controller lift_controller_client.py
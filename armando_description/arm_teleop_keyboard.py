import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys
import select
import termios
import tty

msg = """
Controllo da tastiera per il manipolatore (ARMANDO)
--------------------------------------------------
Usa i tasti per muovere i giunti:
q / a : Giunto 1 (+ / -)
w / s : Giunto 2 (+ / -)
e / d : Giunto 3 (+ / -)
r / f : Giunto 4 (+ / -)

CTRL-C per uscire
"""

joint_names = ['j0', 'j1', 'j2', 'j3'] # Sostituisci con i nomi reali dei tuoi giunti se diversi
joint_positions = [0.0, 0.0, 0.0, 0.0]
step = 0.05

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = rclpy.create_node('arm_teleop_keyboard')
    publisher = node.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

    print(msg)
    try:
        while True:
            key = getKey(settings)
            if key == 'q':
                joint_positions[0] += step
            elif key == 'a':
                joint_positions[0] -= step
            elif key == 'w':
                joint_positions[1] += step
            elif key == 's':
                joint_positions[1] -= step
            elif key == 'e':
                joint_positions[2] += step
            elif key == 'd':
                joint_positions[2] -= step
            elif key == 'r':
                joint_positions[3] += step
            elif key == 'f':
                joint_positions[3] -= step
            elif key == '\x03':
                break

            if key in ['q', 'a', 'w', 's', 'e', 'd', 'r', 'f']:
                traj = JointTrajectory()
                traj.joint_names = joint_names
                point = JointTrajectoryPoint()
                point.positions = list(joint_positions)
                point.time_from_start.sec = 1
                traj.points.append(point)
                publisher.publish(traj)
                print(f"Invio posizioni: {joint_positions}")

    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
import argparse
import os

parser = argparse.ArgumentParser()

demos = ["main", "intro", "voxelmorph", "inverse", "brain_vxm", 'brain_inv', "mnist_vxm", "mnist_inv", "analyses"]
parser.add_argument("-d", "--demo", metavar="NAME", choices=demos, default="main",
                    help="choose a demo to show, among: " + ", ".join(demos))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parser.parse_args()
    os.system(f"streamlit run scripts/demo/demo__{args.demo}.py")

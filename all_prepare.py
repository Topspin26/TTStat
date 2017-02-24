import master_tour_prepare
import bkfon_results_prepare
import ittf_prepare
import kchr_prepare
import propingpong_prepare

def main():
    master_tour_prepare.main()
    bkfon_results_prepare.main()
    propingpong_prepare.main()
    ittf_prepare.main()
    kchr_prepare.main()

if __name__ == "__main__":
    main()
import parser_cas
import parser_coco
import logging

logger = logging.getLogger(__name__)
logfile_handler = logging.FileHandler("../verification_result.txt", mode='w')
logger.addHandler(logfile_handler)

def main():
    coco_lib = parser_coco.Library(path_str='coco_out.txt')
    cas_lib = parser_cas.Library(path_str='../Cycle Accurate Simulator/cas_out.txt')
    
    test_passed = True
    mismatch = 0

    for idx, _ in enumerate(coco_lib.cycles):
        logging.warning(f'Cycle: {coco_lib.cycles[idx].cycle}')
        logging.warning(f'*******Cycle Accurate Simulator Output*******\n{str(cas_lib.cycles[idx])}')
        logging.warning(f'*******cocoTB Verification Output*******\n{str(coco_lib.cycles[idx])}\n')
        if cas_lib.cycles[idx] != coco_lib.cycles[idx]:
            test_passed = False
            mismatch = coco_lib.cycles[idx].cycle
            break

    if test_passed:
        logging.warning('All cycles are identical; BENCHMARK PASSED')
    else:
        logging.warning(f'BENCHMARK FAILED, First mismatch at cycle: {mismatch}')


if __name__ == '__main__':
    main()
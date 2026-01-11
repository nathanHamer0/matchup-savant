from backend.main import get_matchup

# Arbitraraly selected
ERROR_MARGIN = 0.01

def perc_assert(perc: float) -> bool:   # TODO: not used
    return 0.99 <= perc <= 1.01

def ret_assert(ret: float) -> bool:   # TODO: not used
    return ret != None

def main():
    # Neutrality check
    zero_score = get_matchup("neutral", "neutral")
    if abs(zero_score) > ERROR_MARGIN:   
        raise ValueError("NEUTRALITY FAIL")
    
    # Monotonicity check 
    # TODO
    
    print("VALIDATION PASSED")
    
if __name__ == "__main__":
    main()
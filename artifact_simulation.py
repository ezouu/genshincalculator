# artifact_simulation.py

from config import (
    CHARACTER_UNDER_TEST, RESIN_PER_WEEK, RESIN_PER_RUN, ARTIFACTS_PER_RUN, 
    STAT_AVERAGE_DAMAGE, ITERATIONS, STARTING_WEEK, MAX_NUM_WEEKS, BENNETT_ATK_BUFF, PRIORITIZE_STAT
)
from artifact_simulation_utils import (
    simulate_multi_week_artifact_progression
)

# Entry point
simulate_multi_week_artifact_progression(
    CHARACTER_UNDER_TEST, RESIN_PER_WEEK, RESIN_PER_RUN, ARTIFACTS_PER_RUN, 
    STAT_AVERAGE_DAMAGE, ITERATIONS, STARTING_WEEK, MAX_NUM_WEEKS, BENNETT_ATK_BUFF, PRIORITIZE_STAT
)

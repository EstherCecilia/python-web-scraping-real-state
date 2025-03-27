import models.analytics as analytics
import models.process as process
import models.realstate as realState

if __name__ == "__main__":
    realState.get_real_state(61, 60)
    process.process_csv('data/files', 'data/output/real_state.csv')
    analytics.analyze_properties('data/output/real_state.csv')
import statsmodels.api as sm

class DefaultLinearRegressor():
    
    def __init__(self):
        pass
    
    def fit(self, X, y):
        
        X = sm.add_constant(X)
        self.model_object = sm.OLS(y, X).fit()
        
    def predict(self, X):
        
        X = sm.add_constant(X)
        return self.model_object.predict(X)
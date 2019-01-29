# old code


#model = regr.fit(trainRPM, trainRPMY)
#predictions = regr.predict(trainRPM)

#feature_cols = [col for col in train.columns if 'Barrel' not in col]
#x = feature_cols
#print (type(x))
#y = train.pop('Barrel Pressure Before Gas - Pressures').values
#plt.show()
#attributes = ["Barrel Pressure Before Gas - Pressures", "Line Speed (fpm) - Main Measurement", "Adapter (°F) - Co-Poly Temperatures"]
#scatter_matrix(train[attributes], figsize=(12, 8))
#train.drop("Factory time", axis = 1)
#print("Pred:\t", regr.predict())
#from sklearn.preprocessing import OneHotEncoder
#from sklearn.pipeline import Pipeline
#ohe = OneHotEncoder(sparse=False)
#train_transformed = ohe.fit_transform(train)
#train_transformed.shape
#feature_names = ohe.get_feature_names()
#feature_names
#train_inv = ohe.inverse_transform(train_transformed)
#train_inv
#head(2),'\n\n', x.head(2))
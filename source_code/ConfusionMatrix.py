class confusionMatrix:
    
    def __init__(self):
        pass
    
    def recall(self,tp,fn):
        return tp/(tp+fn)
    
    def precision(self,tp,fp):
        return tp/(tp+fp)
    
    def acuracy(self,tp,tn,fp,fn):
        return (tp+tn)/(tp+tn+fp+fn)
    
    def fmeasure(self,recall,precission):
       return 2*(precission*recall)/(precission+recall)
    
    
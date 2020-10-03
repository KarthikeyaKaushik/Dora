rm(list=ls())
library(igraph)
library(viridis)
library(colourvalues)
library(fields)
library(tidyverse)
library(ggplot2)
library(wesanderson)
library(matrixStats)


types_tests = c('google','wordgcn')
result_data = data.frame('mean_fs'=NA,'std_fs'=NA,'var_fs'=NA,'mean_rmse'=NA,
                         'std_rmse'=NA)
violin_data = data.frame('precision'=NA,'embedding_type'=NA)
for (type_test in types_tests){
  rmses = read.table(file.path('~','karthikeya','Dora',
                               'BrPong_1','workspace','karthikeya',
                               'data','results',type_test,
                               paste(type_test,'_rmses.csv',sep='')),
                     header=TRUE,sep=',',row.names = 1)
  fscores = read.table(file.path('~','karthikeya','Dora',
                                   'BrPong_1','workspace','karthikeya',
                                   'data','results',type_test,
                                   paste(type_test,'_fscores.csv',sep='')),
                         header=TRUE,sep=',',row.names = 1)
  mean_fscores = mean(as.numeric(fscores[100,]))
  std_fscores = sd(as.numeric(fscores[100,]))
  var_fscores = var(as.numeric(fscores[100,]))
  mean_rmse = mean(as.numeric(rmses[100,]))
  std_rmse = sd(as.numeric(rmses[100,]))
  result_data = rbind(result_data,c(mean_fscores,std_fscores,var_fscores,
                                    mean_rmse,std_rmse))
  temp = cbind(as.numeric(fscores[100,]),rep(type_test,10))
  colnames(temp) = c('precision','embedding_type')
  violin_data = rbind(violin_data,temp)
}

violin_data = violin_data[-1,]
result_data = result_data[-1,]
result_data$type_embedding = types_tests
# remove sg and cbow
#result_data = result_data[-c(1,2),]
violin_data$precision = as.numeric(violin_data$precision)
violin_plot = ggplot(data=violin_data,aes(x=as.factor(embedding_type),
                                          y=precision)) +
  geom_violin()
plot(violin_plot)



results = ggplot(data=result_data,aes(x=as.factor(type_embedding),
                                      y=mean_fs)) +
  geom_violin(stat='identity',aes(fill=type_embedding)) +
  coord_cartesian(ylim=c(0.5,0.75)) +
  geom_errorbar(aes(ymin=mean_fs-std_fs, ymax=mean_fs+std_fs), width=.2) +
  #scale_fill_manual(values=wes_palette(n=4,name="Cavalcanti1")) + 
  scale_fill_viridis(discrete=TRUE) +
  geom_text(aes(label=round(mean_fs,digits=3)), vjust=-0.3,hjust=1.4, size=3.5) + 
  theme_light() + 
  labs(x='Embeddings', y='Mean precision',fill='Embeddings')
plot(results)
ggsave(file.path('~','karthikeya','Dora',
                 'BrPong_1','workspace','karthikeya',
                 'data','results','fscore_comparison.jpg'))

#### plot learning curve ################
learning_curve = data.frame('fs'=NA,'type_embedding'=NA)
learning_curve = learning_curve[-1,]
types_tests = c('google','wordgcn')
for (type_test in types_tests){
  fscores = read.table(file.path('~','karthikeya','Dora',
                                 'BrPong_1','workspace','karthikeya',
                                 'data','results',type_test,
                                 paste(type_test,'_fscores.csv',sep='')),
                       header=TRUE,sep=',',row.names = 1)
  mean_fs = rowMeans(fscores,na.rm=T)
  sd_fs = rowSds(as.matrix(fscores),na.rm=T)
  learning_curve = rbind.data.frame(learning_curve,
                                    cbind.data.frame(mean_fs,sd_fs,
                                                    1:100,
                                                    rep(type_test,100)))
}



colnames(learning_curve) = c('mean_fs','sd_fs','time_points','type_embedding')
learning_plot = ggplot(data=learning_curve,
                       aes(x=time_points,group=type_embedding)) +
  geom_ribbon(aes(ymin=mean_fs-sd_fs,ymax=mean_fs+sd_fs,
                  fill=type_embedding),alpha=0.5,show.legend = FALSE) +
  geom_line(aes(y=mean_fs,color=type_embedding),size=1) + 
  scale_color_viridis(discrete=TRUE) +
  scale_fill_viridis(discrete=TRUE) +
  theme_light() +
  labs(x='Iterations', y='Mean Precision',fill='Embeddings')
  
plot(learning_plot)
ggsave(file.path('~','karthikeya','Dora',
                 'BrPong_1','workspace','karthikeya',
                 'data','results','learning_comparison.jpg'))

#### plot activation across time ################

filenames_P <- list.files(file.path('~','karthikeya','Dora',
                                  'BrPong_1','workspace','karthikeya',
                                  'data','results','activations','Ps'), 
                                  pattern="*.csv", full.names=TRUE)
filenames_RB <- list.files(file.path('~','karthikeya','Dora',
                                    'BrPong_1','workspace','karthikeya',
                                    'data','results','activations','RBs'), 
                          pattern="*.csv", full.names=TRUE)
filenames_PO <- list.files(file.path('~','karthikeya','Dora',
                                    'BrPong_1','workspace','karthikeya',
                                    'data','results','activations','POs'), 
                          pattern="*.csv", full.names=TRUE)
# to put them in the right order
time_steps = 10 # change as necessary
filenames_P[c(1,2,3:time_steps)] = filenames_P[c(1,3:time_steps,2)] 
filenames_RB[c(1,2,3:time_steps)] = filenames_RB[c(1,3:time_steps,2)]
filenames_PO[c(1,2,3:time_steps)] = filenames_PO[c(1,3:time_steps,2)]

list_P = lapply(filenames_P, read.table)
list_RB = lapply(filenames_RB, read.table)
list_PO = lapply(filenames_PO, read.table)

activation_dataframe = data.frame('val'=NA,'unit_type'=NA,'time_step'=NA)
activation_dataframe = activation_dataframe[-1,]
time_steps = length(list_P) # number of samples

for (time_step in 1:time_steps){
  current_df = as.data.frame(list_P[time_step])
  print(colSums(current_df))
  temp_df = cbind.data.frame(colSums(current_df),
                             'P',time_step*10)
  colnames(temp_df) = c('val','unit_type','time_step')
  activation_dataframe = rbind.data.frame(activation_dataframe,temp_df)
}
for (time_step in 1:time_steps){
  current_df = as.data.frame(list_RB[time_step])
  temp_df = cbind.data.frame(colSums(current_df),
                             'RB',time_step*10)
  colnames(temp_df) = c('val','unit_type','time_step')
  activation_dataframe = rbind.data.frame(activation_dataframe,temp_df)
}
for (time_step in 1:time_steps){
  current_df = as.data.frame(list_PO[time_step])
  temp_df = cbind.data.frame(colSums(current_df),
                             'PO',time_step*10)
  colnames(temp_df) = c('val','unit_type','time_step')
  activation_dataframe = rbind.data.frame(activation_dataframe,temp_df)
}


activation_dataframe$val = log10(activation_dataframe$val)
activation_dataframe$unit_type = as.factor(activation_dataframe$unit_type)
activation_dataframe$time_step = as.factor(activation_dataframe$time_step)
colnames(activation_dataframe) = c('val','unit_type','iteration')
#activation_dataframe = reshape(activation_dataframe,direction='wide',
#                               idvar='iteration',timevar='unit_type')
#colnames(activation_dataframe) = c('iteration','valP','valRB','valPO')
activation_plot = ggplot(data=activation_dataframe,
                         aes(x=iteration,y=unit_type)) + 
  geom_bar(aes(fill=val,y=1),stat='identity') + 
  scale_fill_viridis('Activation',direction=-1) + 
  theme_light() +
  theme(axis.ticks=element_blank(),
       axis.text.y=element_blank(),
       panel.grid = element_blank()) + labs(y='Unit types')  +
  facet_grid(unit_type ~ .)
plot(activation_plot)
ggsave(file.path('~','karthikeya','Dora',
                 'BrPong_1','workspace','karthikeya',
                 'data','results','coactivation.jpg'))






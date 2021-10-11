//var color = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
//这部分模拟数据库传来的数据，只是无法交互更新
var categories = [{
	name: 0,

}, {
	name: 1,

}, {
	name: 2,

}, {
	name: 3,

}, {
	name: 4,

}, {
	name: 5,

}]
//var graph = {
//	data: [{
//		name: 'ArtificialIntelligence',
//		category: 0,
//		number: 0,
//		itemStyle: {
//			normal: {
//				//	color: "#009800",
//				opacity: 1
//
//			}
//		}
//	}, {
//		name: 'DataMining',
//		number: 1,
//		category: 1,
//
//		itemStyle: {
//			normal: {
//				opacity: 1
//			}
//		}
//	}, {
//		name: 'MachineLearning',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'ComputerVision',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'NaturalLanguageProcessing',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'Robotics',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'InformationRetrieval',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'Human-ComputerInteraction',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'AnomalyDetection',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'AssociationRuleLearning',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'Clustering',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'Classification',
//
//		category: 1,
//		// draggable: true,
//	}, {
//		name: 'Regression',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'Summarization',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'Embedding',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'NetworkEmbedding',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'SupervisedLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'UnsupervisedLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'Semi-SupervisedLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'ReinforcementLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'SelfLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'FederatedLearning',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'DecisionTrees',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'SupportVectorMachines',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'RegressionAnalysis',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'BayesianNetworks',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'GeneticAlgorithms',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'GraphNeuralNetworks',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'SpectralEmbedding',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'Recognition',
//
//		category: 1,
//		//  draggable: true,
//	}, {
//		name: 'MotionAnalysis',
//
//		category: 1,
//		//  draggable: true,
//	},
//	{name: 'SceneReconstruction',category: 1},
//	{name: 'ImageRestoration',category: 1},
//	{name: 'COMP1433',category: 2},
//	{name: 'DataProcessing',category: 2},
//	{name: 'StatisticalAnalysis',category: 2},
//	{name: 'LinearAlgebra',category: 2},
//	{name: 'Calculus',category: 2},
//	{name: 'DataCollection',category: 2},
//	{name: 'DataVisualization',category: 2},
//	{name: 'DataCleansing',category: 2},
//	{name: 'LinearRegression',category: 2},
//	{name: 'TimeSeriesAnalysis',category: 2},
//	{name: 'VectorSpace',category: 2},
//	{name: 'Matrix',category: 2},
//	{name: 'Integral',category: 2},
//	{name: 'COMP2011',category: 3},
//	{name: 'LinearDataStructures',category: 3},
//	{name: 'TreeDataStructure',category: 3},
//	{name: 'AlgorithmsGenerals',category: 3},
//	{name: 'SortingSlgorithm',category: 3},
//	{name: 'SearchAlgorithm',category: 3},
//	{name: 'COMP3133',category: 4},
//	{name: 'MorphologicalAnalysis',category: 4},
//	{name: 'NLPApplications',category: 4},
//	{name: 'Stemming',category: 4},
//	{name: 'IntroductionToAI',category: 5},
//	{name: 'COMP4431',category: 5},
//	{name: 'HistoryOfAI',category: 5},
//	{name: 'DefinitionOfAI',category: 5},
//	{name: 'EthicalIssuesOfAI',category: 5},
//	{name: 'COMP4432',category: 5}
//	],
//	links: [{
//		source: 'ArtificialIntelligence',
//		target: 'DataMining',
//
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'MachineLearning',
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'ComputerVision',
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'NaturalLanguageProcessing',
//
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'Robotics',
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'InformationRetrieval',
//	}, {
//		source: 'ArtificialIntelligence',
//		target: 'Human-ComputerInteraction',
//
//	}, {
//		source: 'DataMining',
//		target: 'AnomalyDetection',
//	}, {
//		source: 'DataMining',
//		target: 'AssociationRuleLearning',
//	}, {
//		source: 'DataMining',
//		target: 'Clustering',
//
//	}, {
//		source: 'DataMining',
//		target: 'Classification',
//	}, {
//		source: 'DataMining',
//		target: 'Regression',
//	}, {
//		source: 'DataMining',
//		target: 'Summarization',
//	}, {
//		source: 'DataMining',
//		target: 'Embedding',
//
//	}, {
//		source: 'Embedding',
//		target: 'NetworkEmbedding',
//	}, {
//		source: 'MachineLearning',
//		target: 'SupervisedLearning',
//	}, {
//		source: 'MachineLearning',
//		target: 'UnsupervisedLearning',
//	}, {
//		source: 'MachineLearning',
//		target: 'Semi-SupervisedLearning',
//
//	}, {
//		source: 'MachineLearning',
//		target: 'ReinforcementLearning',
//	}, {
//		source: 'MachineLearning',
//		target: 'SelfLearning',
//	}, {
//		source: 'MachineLearning',
//		target: 'AnomalyDetection',
//	}, {
//		source: 'MachineLearning',
//		target: 'AssociationRuleLearning',
//
//	}, {
//		source: 'MachineLearning',
//		target: 'Clustering',
//	}, {
//		source: 'MachineLearning',
//		target: 'Classification',
//	}, {
//		source: 'MachineLearning',
//		target: 'Regression',
//	}, {
//		source: 'MachineLearning',
//		target: 'Embedding',
//
//	}, {
//		source: 'MachineLearning',
//		target: 'FederatedLearning',
//	}, {
//		source: 'MachineLearning',
//		target: 'DecisionTrees',
//	}, {
//		source: 'MachineLearning',
//		target: 'SupportVectorMachines',
//	}, {
//		source: 'MachineLearning',
//		target: 'RegressionAnalysis',
//
//	}, {
//		source: 'MachineLearning',
//		target: 'BayesianNetworks',
//	}, {
//		source: 'MachineLearning',
//		target: 'GeneticAlgorithms',
//	}, {
//		source: 'NetworkEmbedding',
//		target: 'GraphNeuralNetworks',
//	},
//	{source: 'NetworkEmbedding',target: 'SpectralEmbedding'},
//	{source: 'ComputerVision',target: 'Recognition'},
//	{source: 'ComputerVision',target: 'MotionAnalysis'},
//	{source: 'ComputerVision',target: 'SceneReconstruction'},
//	{source: 'ComputerVision',target: 'ImageRestoration'},
//	{source: 'COMP1433',target: 'DataProcessing'},
//	{source: 'COMP1433',target: 'StatisticalAnalysis'},
//	{source: 'COMP1433',target: 'LinearAlgebra'},
//	{source: 'COMP1433',target: 'Calculus'},
//	{source: 'DataProcessing',target: 'DataCollection'},
//	{source: 'DataProcessing',target: 'DataVisualization'},
//	{source: 'DataProcessing',target: 'DataCleansing'},
//	{source: 'StatisticalAnalysis',target: 'LinearRegression'},
//	{source: 'StatisticalAnalysis',target: 'TimeSeriesAnalysis'},
//	{source: 'LinearAlgebra',target: 'VectorSpace'},
//	{source: 'LinearAlgebra',target: 'Matrix'},
//	{source: 'Calculus',target: 'Integral'},
//	{source: 'COMP2011',target: 'LinearDataStructures'},
//	{source: 'COMP2011',target: 'TreeDataStructure'},
//	{source: 'COMP2011',target: 'AlgorithmsGenerals'},
//	{source: 'AlgorithmsGenerals',target: 'SortingSlgorithm'},
//	{source: 'AlgorithmsGenerals',target: 'SearchAlgorithm'},
//	{source: 'COMP3133',target: 'MorphologicalAnalysis'},
//	{source: 'COMP3133',target: 'NLPApplications'},
//	{source: 'MorphologicalAnalysis',target: 'Stemming'},
//	{source: 'COMP4431',target: 'IntroductionToAI'},
//	{source: 'COMP4431',target: 'MachineLearning'},
//	{source: 'IntroductionToAI',target: 'HistoryOfAI'},
//	{source: 'IntroductionToAI',target: 'DefinitionOfAI'},
//	{source: 'IntroductionToAI',target: 'EthicalIssuesOfAI'},
//	{source: 'COMP4432',target: 'MachineLearning'}
//	]
//}
var graph = {'data': [{'name': 'Knowledgebase', 'category': 4}, {'name': 'Ethicsofartificialintelligence', 'category': 4}, {'name': 'Pragmatics', 'category': 0}, {'name': 'Graphicalmodel', 'category': 0}, {'name': 'Binarysearchtree', 'category': 2}, {'name': 'Bayesiannetwork', 'category': 0}, {'name': 'Statisticalclassification', 'category': 0}, {'name': 'Supervisedlearning', 'category': 0}, {'name': 'Informationretrieval(basics)', 'category': 0}, {'name': 'Dialoguesystem', 'category': 3}, {'name': 'Federatedlearning', 'category': 0}, {'name': 'Knowledgebasedsystems', 'category': 4}, {'name': 'Dataanalysis(basics)', 'category': 0}, {'name': 'Imagerestoration', 'category': 0}, {'name': 'Unsupervisedlearning', 'category': 0}, {'name': 'Naturallanguagegeneration', 'category': 0}, {'name': 'Listofalgorithms', 'category': 2}, {'name': 'COMP4133', 'category': 4}, {'name': 'COMP1011', 'category': 1}, {'name': 'Queue(abstractdatatype)', 'category': 2}, {'name': 'Insertionsort', 'category': 2}, {'name': 'Naturallanguageprocessing(basics)', 'category': 1}, {'name': 'Mergesort', 'category': 2}, {'name': 'Backwardchaining', 'category': 4}, {'name': 'List(abstractdatatype)', 'category': 2}, {'name': 'Timeseriesanalysis', 'category': 1}, {'name': 'Datacollection', 'category': 1}, {'name': 'Naturallanguageprocessing', 'category': 0}, {'name': 'Sentimentanalysis', 'category': 3}, {'name': 'Spectralclustering', 'category': 0}, {'name': 'Automatedplanningandscheduling', 'category': 0}, {'name': 'Robotics', 'category': 0}, {'name': 'COMP3133', 'category': 3}, {'name': 'Dataprocessing', 'category': 0}, {'name': 'Networkembedding', 'category': 0}, {'name': 'Parsing', 'category': 3}, {'name': 'Semisupervisedlearning', 'category': 0}, {'name': 'Morphology(linguistics)', 'category': 0}, {'name': '3Dreconstruction', 'category': 0}, {'name': 'Semanticanalysis(machinelearning)', 'category': 0}, {'name': 'Dataanalysis', 'category': 0}, {'name': 'Linearregression', 'category': 1}, {'name': 'Sortingalgorithm', 'category': 2}, {'name': 'Geneticalgorithm', 'category': 0}, {'name': 'Discourseanalysis', 'category': 3}, {'name': 'Coreference', 'category': 3}, {'name': 'Worldwideweb', 'category': 0}, {'name': 'Computerdatastorage', 'category': 0}, {'name': 'Languagemodel', 'category': 0}, {'name': 'Abstractdatatype', 'category': 2}, {'name': 'Listofdatastructures', 'category': 2}, {'name': 'Quicksort', 'category': 2}, {'name': 'Booleanmodelofinformationretrieval', 'category': 4}, {'name': 'Decisiontree', 'category': 0}, {'name': 'Intelligentagent', 'category': 4}, {'name': 'Featurelearning', 'category': 0}, {'name': 'Artificialintelligence(basics)', 'category': 0}, {'name': 'Forwardchaining', 'category': 4}, {'name': 'Selectionsort', 'category': 2}, {'name': 'Integral', 'category': 1}, {'name': 'Dimensionalityreduction', 'category': 0}, {'name': 'Stemming', 'category': 0}, {'name': 'Vectorspace', 'category': 1}, {'name': 'Machinetranslation', 'category': 0}, {'name': 'Binarytree', 'category': 2}, {'name': 'Informationretrieval', 'category': 0}, {'name': 'Lexicalsemantics', 'category': 0}, {'name': 'Statistics(basics)', 'category': 0}, {'name': 'Database', 'category': 0}, {'name': 'Statistics', 'category': 0}, {'name': 'Computervision', 'category': 0}, {'name': 'Decisionsupportsystem', 'category': 0}, {'name': 'Inferenceengine', 'category': 4}, {'name': 'Reinforcementlearning', 'category': 0}, {'name': 'Speechrecognition', 'category': 0}, {'name': 'Matrix(mathematics)', 'category': 1}, {'name': 'Multitasklearning', 'category': 0}, {'name': 'Activelearning(machinelearning)', 'category': 0}, {'name': 'Calculus', 'category': 1}, {'name': 'COMP2411', 'category': 2}, {'name': 'Searchalgorithm', 'category': 2}, {'name': 'Knowledgerepresentationandreasoning', 'category': 0}, {'name': 'ArtificialIntelligence', 'category': 0}, {'name': 'Linearsearch', 'category': 2}, {'name': 'Phonology', 'category': 0}, {'name': 'Machinelearning', 'category': 0}, {'name': 'Tree(datastructure)', 'category': 2}, {'name': 'Searchtree', 'category': 2}, {'name': 'Distributedartificialintelligence', 'category': 0}, {'name': 'NLPapplications', 'category': 0}, {'name': 'Artificialintelligence', 'category': 0}, {'name': 'Activityrecognition', 'category': 0}, {'name': 'Informationextraction', 'category': 0}, {'name': 'Imagesegmentation', 'category': 0}, {'name': 'Informationsystem', 'category': 0}, {'name': 'Languageresource', 'category': 0}, {'name': 'Wordsensedisambiguation', 'category': 3}, {'name': 'Linearalgebra', 'category': 1}, {'name': 'Binarysearchalgorithm', 'category': 2}, {'name': 'COMP1433', 'category': 1}, {'name': 'Deeplearning', 'category': 0}, {'name': 'Objectdetection', 'category': 0}, {'name': 'Automaticsummarization', 'category': 0}, {'name': 'Bubblesort', 'category': 2}, {'name': 'Nil', 'category': 1}, {'name': 'Associationrulelearning', 'category': 0}, {'name': 'Chinesecharacterencoding', 'category': 3}, {'name': 'Clusteranalysis', 'category': 0}, {'name': 'Informationretrievalmodels', 'category': 4}, {'name': 'Datastructures', 'category': 0}, {'name': 'AIcontrolproblem', 'category': 0}, {'name': 'COMP2011', 'category': 2}, {'name': 'Stack(abstractdatatype)', 'category': 2}, {'name': 'Anomalydetection', 'category': 0}, {'name': 'Supportvectormachine', 'category': 0}, {'name': 'Regressionanalysis', 'category': 0}, {'name': 'Questionanswering', 'category': 3}, {'name': 'COMP4431', 'category': 4}, {'name': 'Historyofartificialintelligence', 'category': 4}, {'name': 'Visualinspection', 'category': 0}, {'name': 'Arraydatastructure', 'category': 2}, {'name': 'Linkedlist', 'category': 2}, {'name': 'Graphneuralnetwork', 'category': 0}, {'name': 'Contentbasedimageretrieval', 'category': 0}, {'name': 'Enterpriseinformationsystem', 'category': 0}, {'name': 'Datamining', 'category': 0}, {'name': 'Motionanalysis', 'category': 0}, {'name': 'Datavisualization', 'category': 1}, {'name': 'Datacleansing', 'category': 1}, {'name': 'Philosophyofartificialintelligence', 'category': 0}], 'links': [{'source': 'Semanticanalysis(machinelearning)', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'List(abstractdatatype)', 'target': 'Abstractdatatype'}, {'source': 'NLPapplications', 'target': 'Naturallanguageprocessing'}, {'source': 'Naturallanguageprocessing(basics)', 'target': 'COMP3133'}, {'source': 'Automaticsummarization', 'target': 'Datamining'}, {'source': 'COMP2011', 'target': 'COMP4431'}, {'source': 'Dataprocessing', 'target': 'Dataanalysis'}, {'source': 'Pragmatics', 'target': 'Naturallanguageprocessing'}, {'source': 'Linearregression', 'target': 'Statistics'}, {'source': 'Morphology(linguistics)', 'target': 'Naturallanguageprocessing'}, {'source': 'Anomalydetection', 'target': 'Machinelearning'}, {'source': 'Tree(datastructure)', 'target': 'COMP2011'}, {'source': 'Activelearning(machinelearning)', 'target': 'Machinelearning'}, {'source': 'Listofdatastructures', 'target': 'COMP2011'}, {'source': 'Sentimentanalysis', 'target': 'NLPapplications'}, {'source': 'Machinelearning', 'target': 'COMP4431'}, {'source': 'Booleanmodelofinformationretrieval', 'target': 'Informationretrieval'}, {'source': 'Multitasklearning', 'target': 'Machinelearning'}, {'source': 'AIcontrolproblem', 'target': 'Artificialintelligence'}, {'source': 'Naturallanguagegeneration', 'target': 'Naturallanguageprocessing'}, {'source': 'Informationretrieval', 'target': 'ArtificialIntelligence'}, {'source': 'Graphneuralnetwork', 'target': 'Networkembedding'}, {'source': 'Vectorspace', 'target': 'Linearalgebra'}, {'source': 'Worldwideweb', 'target': 'Informationsystem'}, {'source': 'Associationrulelearning', 'target': 'Datamining'}, {'source': 'Deeplearning', 'target': 'Machinelearning'}, {'source': 'Informationretrieval', 'target': 'Informationsystem'}, {'source': 'Stack(abstractdatatype)', 'target': 'Abstractdatatype'}, {'source': 'Informationretrieval(basics)', 'target': 'Informationretrieval'}, {'source': 'Anomalydetection', 'target': 'Computervision'}, {'source': 'Linkedlist', 'target': 'Listofdatastructures'}, {'source': 'Contentbasedimageretrieval', 'target': 'Computervision'}, {'source': 'Morphology(linguistics)', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Ethicsofartificialintelligence', 'target': 'Artificialintelligence(basics)'}, {'source': 'Graphicalmodel', 'target': 'Machinelearning'}, {'source': 'Intelligentagent', 'target': 'COMP4431'}, {'source': 'Clusteranalysis', 'target': 'Datamining'}, {'source': 'Activityrecognition', 'target': 'Computervision'}, {'source': 'Naturallanguageprocessing(basics)', 'target': 'Naturallanguageprocessing'}, {'source': 'NLPapplications', 'target': 'COMP3133'}, {'source': 'Reinforcementlearning', 'target': 'Machinelearning'}, {'source': 'Dataprocessing', 'target': 'COMP1433'}, {'source': 'Searchalgorithm', 'target': 'COMP2011'}, {'source': 'Bayesiannetwork', 'target': 'Graphicalmodel'}, {'source': 'Wordsensedisambiguation', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Motionanalysis', 'target': 'Computervision'}, {'source': 'Binarytree', 'target': 'Tree(datastructure)'}, {'source': 'Datamining', 'target': 'Informationsystem'}, {'source': 'Unsupervisedlearning', 'target': 'Machinelearning'}, {'source': 'Chinesecharacterencoding', 'target': 'COMP3133'}, {'source': 'Clusteranalysis', 'target': 'Machinelearning'}, {'source': 'Informationretrievalmodels', 'target': 'COMP4133'}, {'source': 'Languageresource', 'target': 'Naturallanguageprocessing'}, {'source': 'COMP2411', 'target': 'COMP4133'}, {'source': 'Robotics', 'target': 'ArtificialIntelligence'}, {'source': 'Sortingalgorithm', 'target': 'COMP2011'}, {'source': 'Phonology', 'target': 'Naturallanguageprocessing'}, {'source': 'Linearalgebra', 'target': 'COMP1433'}, {'source': 'Datacollection', 'target': 'Dataprocessing'}, {'source': 'Regressionanalysis', 'target': 'Datamining'}, {'source': 'Binarysearchalgorithm', 'target': 'Searchalgorithm'}, {'source': 'Binarysearchtree', 'target': 'Searchtree'}, {'source': 'Machinetranslation', 'target': 'Naturallanguageprocessing'}, {'source': 'Imagerestoration', 'target': 'Computervision'}, {'source': 'Distributedartificialintelligence', 'target': 'Artificialintelligence'}, {'source': 'Informationextraction', 'target': 'Naturallanguageprocessing'}, {'source': 'Calculus', 'target': 'COMP1433'}, {'source': 'Naturallanguageprocessing', 'target': 'Artificialintelligence'}, {'source': 'Searchtree', 'target': 'Tree(datastructure)'}, {'source': 'Regressionanalysis', 'target': 'Machinelearning'}, {'source': 'Computerdatastorage', 'target': 'Informationsystem'}, {'source': 'Knowledgerepresentationandreasoning', 'target': 'Artificialintelligence'}, {'source': 'Anomalydetection', 'target': 'Datamining'}, {'source': 'COMP1011', 'target': 'COMP3133'}, {'source': 'Historyofartificialintelligence', 'target': 'Artificialintelligence(basics)'}, {'source': 'Questionanswering', 'target': 'NLPapplications'}, {'source': 'Automatedplanningandscheduling', 'target': 'Artificialintelligence'}, {'source': 'Abstractdatatype', 'target': 'COMP2011'}, {'source': 'Geneticalgorithm', 'target': 'Machinelearning'}, {'source': 'Integral', 'target': 'Calculus'}, {'source': 'Networkembedding', 'target': 'Dimensionalityreduction'}, {'source': 'Timeseriesanalysis', 'target': 'Statistics'}, {'source': 'Quicksort', 'target': 'Sortingalgorithm'}, {'source': 'Datastructures', 'target': 'Informationsystem'}, {'source': 'COMP1011', 'target': 'COMP2011'}, {'source': 'Automaticsummarization', 'target': 'NLPapplications'}, {'source': 'Insertionsort', 'target': 'Sortingalgorithm'}, {'source': '3Dreconstruction', 'target': 'Computervision'}, {'source': 'Dataanalysis(basics)', 'target': 'Dataanalysis'}, {'source': 'Enterpriseinformationsystem', 'target': 'Informationsystem'}, {'source': 'Tree(datastructure)', 'target': 'Listofdatastructures'}, {'source': 'Linearsearch', 'target': 'Searchalgorithm'}, {'source': 'Informationextraction', 'target': 'NLPapplications'}, {'source': 'Decisionsupportsystem', 'target': 'Informationsystem'}, {'source': 'Objectdetection', 'target': 'Computervision'}, {'source': 'Statisticalclassification', 'target': 'Machinelearning'}, {'source': 'Computervision', 'target': 'Artificialintelligence'}, {'source': 'Automaticsummarization', 'target': 'Computervision'}, {'source': 'Decisiontree', 'target': 'Machinelearning'}, {'source': 'Parsing', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Binarysearchtree', 'target': 'Binarytree'}, {'source': 'Associationrulelearning', 'target': 'Machinelearning'}, {'source': 'Artificialintelligence(basics)', 'target': 'Artificialintelligence'}, {'source': 'Bubblesort', 'target': 'Sortingalgorithm'}, {'source': 'Federatedlearning', 'target': 'Machinelearning'}, {'source': 'Languagemodel', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Dialoguesystem', 'target': 'NLPapplications'}, {'source': 'COMP2011', 'target': 'COMP4133'}, {'source': 'Artificialintelligence(basics)', 'target': 'COMP4431'}, {'source': 'Philosophyofartificialintelligence', 'target': 'Artificialintelligence'}, {'source': 'Discourseanalysis', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Languagemodel', 'target': 'Naturallanguageprocessing'}, {'source': 'Datavisualization', 'target': 'Dataprocessing'}, {'source': 'Database', 'target': 'Informationsystem'}, {'source': 'Lexicalsemantics', 'target': 'Naturallanguageprocessing'}, {'source': 'Backwardchaining', 'target': 'Inferenceengine'}, {'source': 'Datamining', 'target': 'ArtificialIntelligence'}, {'source': 'Semisupervisedlearning', 'target': 'Machinelearning'}, {'source': 'Semanticanalysis(machinelearning)', 'target': 'Machinelearning'}, {'source': 'Machinetranslation', 'target': 'NLPapplications'}, {'source': 'Forwardchaining', 'target': 'Inferenceengine'}, {'source': 'Datamining', 'target': 'Dataanalysis'}, {'source': 'Supportvectormachine', 'target': 'Machinelearning'}, {'source': 'Featurelearning', 'target': 'Machinelearning'}, {'source': 'Supervisedlearning', 'target': 'Machinelearning'}, {'source': 'Statistics(basics)', 'target': 'Statistics'}, {'source': 'Knowledgebasedsystems', 'target': 'COMP4431'}, {'source': 'Knowledgebase', 'target': 'Knowledgebasedsystems'}, {'source': 'Selectionsort', 'target': 'Sortingalgorithm'}, {'source': 'Speechrecognition', 'target': 'Naturallanguageprocessing'}, {'source': 'Dimensionalityreduction', 'target': 'Datamining'}, {'source': 'Machinelearning', 'target': 'Artificialintelligence'}, {'source': 'Mergesort', 'target': 'Sortingalgorithm'}, {'source': 'Statistics(basics)', 'target': 'COMP1433'}, {'source': 'Imagesegmentation', 'target': 'Computervision'}, {'source': 'Informationretrieval(basics)', 'target': 'COMP4133'}, {'source': 'Arraydatastructure', 'target': 'Listofdatastructures'}, {'source': 'Stemming', 'target': 'Morphology(linguistics)'}, {'source': 'Listofalgorithms', 'target': 'COMP2011'}, {'source': 'Datacleansing', 'target': 'Dataprocessing'}, {'source': 'Coreference', 'target': 'Naturallanguageprocessing(basics)'}, {'source': 'Nil', 'target': 'COMP1433'}, {'source': 'Queue(abstractdatatype)', 'target': 'Abstractdatatype'}, {'source': 'Statisticalclassification', 'target': 'Datamining'}, {'source': 'Knowledgerepresentationandreasoning', 'target': 'COMP4431'}, {'source': 'Inferenceengine', 'target': 'Knowledgebasedsystems'}, {'source': 'Spectralclustering', 'target': 'Networkembedding'}, {'source': 'Dimensionalityreduction', 'target': 'Machinelearning'}, {'source': 'Visualinspection', 'target': 'Computervision'}, {'source': 'Dataprocessing', 'target': 'Datamining'}, {'source': 'Matrix(mathematics)', 'target': 'Linearalgebra'}]}

//var graph =
//var rela = { "data": [], "links": [] };
//    $.getJSON('/all_kg', function (json) {
//        graph = json;
//    });

var optionFromDB = {
	series: [{
		color: ['#9ccc65', '#f2b368', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'],
		draggable: true,
		label: {
			show: true,
			position: 'bottom',
			formatter: '{b}'
		},
		force: {
			repulsion: 100
		},
		data: graph.data,
		links: graph.links,
		categories: categories,
		roam: true,
		//   type: 'graph',      
		//   layout: 'force',
		//  symbolSize: 34,
		//   animationDurationUpdate: 750

	}]
}
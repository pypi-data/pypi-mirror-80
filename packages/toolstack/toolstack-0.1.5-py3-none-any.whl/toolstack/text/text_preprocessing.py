import re
import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm
tqdm.pandas()


class TextPreprocessing:
    """
    Clean and preprocess your text data
    """

    @staticmethod
    def text_case(df, columns, case='lower', verbose=True):
        """
        Perform string manipulation to convert text to/from:
        1. Lower case
        2. Upper case
        3. Capitalize

        Parameters
        ----------
        df : DataFrame
            The df to perform case operation on
        column : string, int
            The column on which the operation has to be performed
        case : string, default 'lower'
            Options: 'lower' , 'upper', 'capitalize'

        Returns
        -------
        List
        """
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"

        for column in columns:
            assert column in df.columns, f"The column: <{column}> is not present in the DataFrame, pass a valid column name"

        __cleaned_data__df = pd.DataFrame()

        for column in columns:
            if not verbose:
                if case.lower() == 'lower':
                    __cleaned_data__df[f'{column}'] = df[column].apply(lambda x: x.lower())
                elif case.lower() == 'upper':
                    __cleaned_data__df[f'{column}'] = df[column].apply(lambda x: x.upper())
                elif case.lower() == 'capitalize':
                    __cleaned_data__df[f'{column}'] = df[column].apply(lambda x: x.capitalize())

            else:
                if case.lower() == 'lower':
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(lambda x: x.lower())
                elif case.lower() == 'upper':
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(lambda x: x.upper())
                elif case.lower() == 'capitalize':
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(lambda x: x.capitalize())

        return __cleaned_data__df

    @staticmethod
    def remove_punctuations(df, columns, regex=r'[^\w\s]', space=False, verbose=True):
        """
        Clean text, remove punctuations and symbols

        Parameters
        ----------
        df : DataFrame
            The df to perform case operation on
        columns : List
            The column on which the operation has to be performed
        regex : string, default r'[^\w\s]'
            Pass any regex to clean the text (punctuations) else leave default
        space : Boolean, default False
            If True, replaces with a space

        Returns
        -------
        List
        """
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"
        for column in columns:
            assert column in df.columns, f"The column: <{column}> is not present in the DataFrame, pass a valid column name"

        __cleaned_data__df = pd.DataFrame()

        for column in columns:
            if not verbose:
                if space:
                    __cleaned_data__df[f'{column}'] = df[column].apply(
                        lambda x: re.sub(regex, ' ', x))
                else:
                    __cleaned_data__df[f'{column}'] = df[column].apply(
                        lambda x: re.sub(regex, '', x))
            else:
                if space:
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                        lambda x: re.sub(regex, ' ', x))
                else:
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                        lambda x: re.sub(regex, '', x))

        return __cleaned_data__df

    @staticmethod
    def remove_digits(df, columns, verbose=True):
        """
        Clean text, remove digits

        Parameters
        ----------
        df : DataFrame
            The df to perform case operation on
        column : string, int
            The column on which the operation has to be performed
        Returns
        -------
        List
        """
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"
        for column in columns:
            assert column in df.columns, f"The column: <{column}> is not present in the DataFrame, pass a valid column name"

        __cleaned_data__df = pd.DataFrame()

        for column in columns:
            if not verbose:
                __cleaned_data__df[f'{column}'] = df[column].apply(
                    lambda x: ' '.join([x for x in x.split() if not x.isdigit()]))
            else:
                __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                    lambda x: ' '.join([x for x in x.split() if not x.isdigit()]))

        return __cleaned_data__df

    @staticmethod
    def remove_characters(df, columns, char=2, verbose=True):
        """
        Clean text, remove char

        Parameters
        ----------
        df : DataFrame
            The df to perform case operation on
        column : string, int
            The column on which the operation has to be performed
        char : int
            Characters below this threshold will be removed 
            
        Returns
        -------
        List
        """
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"
        for column in columns:
            assert column in df.columns, f"The column: <{column}> is not present in the DataFrame, pass a valid column name"

        __cleaned_data__df = pd.DataFrame()

        for column in columns:
            if not verbose:
                __cleaned_data__df[f'{column}'] = df[column].apply(
                    lambda x: ' '.join([x for x in x.split() if len(x.strip()) > char]))
            else:
                __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                    lambda x: ' '.join([x for x in x.split() if len(x.strip()) > char]))

        return __cleaned_data__df

    @staticmethod
    def remove_stopwords(df, columns, verbose=True, **kwargs):
        """
        Remove stopwords from a corpus

        Parameters
        ----------
        df : DataFrame
            The df to perform case operation on
        column : string, int
            The column on which the operation has to be performed
        stopwords : List
            List of stopwords to remove; default list can be found at:
            from toolstack import utils
            stopwords = list(utils.load_stopwords())

        Returns
        -------
        List

        """
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"
        for column in columns:
            assert column in df.columns, f"The column: <{column}> is not present in the DataFrame, pass a valid column name"
        assert ('stopwords' in kwargs.keys() or isinstance(kwargs['stopwords'], list)), "Pass a list of 'stopwords'"

        __cleaned_data__df = pd.DataFrame()

        for column in columns:
            if not verbose:
                if 'text_lower' in kwargs.keys() and kwargs['text_lower']:
                    __cleaned_data__df[f'{column}'] = df[column].apply(
                        lambda x: ' '.join([s.lower() for s in x.split() if s.lower() not in set(kwargs['stopwords'])]))
                else:
                    __cleaned_data__df[f'{column}'] = df[column].apply(
                        lambda x: ' '.join([s for s in x.split() if s.lower() not in set(kwargs['stopwords'])]))
            else:
                if 'text_lower' in kwargs.keys() and kwargs['text_lower']:
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                        lambda x: ' '.join([s.lower() for s in x.split() if s.lower() not in set(kwargs['stopwords'])]))
                else:
                    __cleaned_data__df[f'{column}'] = df[column].progress_apply(
                        lambda x: ' '.join([s for s in x.split() if s.lower() not in set(kwargs['stopwords'])]))

        return __cleaned_data__df



def word_count(df, column, sort='ascending', **kwargs):
    """
    Take the count of unique words

    Parameters
    ----------
    df : DataFrame
        The df to perform case operation on.
    column : string, int
        The column selected should be present in the Dataframe passed
    sort : string, default ascending
        Options: ascending, descending
        If sorted, it will sort values by the count
    stopwords : List
        List of stopwords to remove; default list can be found at:
        from toolstack import utils
        stopwords = list(utils.load_stopwords())

    Returns
    -------
    DataFrame: columns:['Words', 'Count']

    """
    assert isinstance(df, pd.DataFrame), "Pass a DataFrame"
    assert column in df, "The column is not present in the DataFrame, pass a valid column name"

    if 'stopwords' in kwargs.keys():
        assert (isinstance(kwargs['stopwords'], list)), "Pass a list of 'stopwords'"
        word_counter = []
        for x in np.array(df[column]):
            x = x.split()
            for word in x:
                if word.lower() not in set(kwargs['stopwords']):
                    word_counter.append(word.lower())
        k_v = Counter(word_counter)
    else:
        word_counter = []
        for x in np.array(df[column]):
            x = x.split()
            for word in x:
                word_counter.append(word.lower())
        k_v = Counter(word_counter)

    if sort == 'ascending':
        return (pd.DataFrame({'Words': [x for x in k_v.keys()], 'Count': [x for x in k_v.values()]})).sort_values(
            'Count')
    elif sort == 'descending':
        return (pd.DataFrame({'Words': [x for x in k_v.keys()], 'Count': [x for x in k_v.values()]})).sort_values(
            'Count', ascending=False)
    else:
        return pd.DataFrame({'Words': [x for x in k_v.keys()], 'Count': [x for x in k_v.values()]})


class AutomatedTextPreprocessing(TextPreprocessing):

    """
    Perform Automated Data Pre-processing on textual data.

    Parameters
    ----------
    df : DataFrame
        The df to perform case operation on.
    column : List
        The columns in the list should be present in the Dataframe passed

    """

    def __init__(self, df):
        assert isinstance(df, pd.DataFrame), "Pass a DataFrame"

        super(AutomatedTextPreprocessing, self).__init__()
        self.df = df.copy()
        self.columns = [str(x) for x in self.df.columns]
        self.df.columns = self.columns
        self.stopwords = set(
            pd.read_csv('https://algs4.cs.princeton.edu/35applications/stopwords.txt', header=None)[0].values.tolist()
        )
        self.char = 2
        self.df_cleaned = pd.DataFrame()

    def stack(self):
        for column in self.columns:
            if self.df[column].dtype == 'O':
                self.df_cleaned[column] = self.text_case(self.df, [column])[column]
                self.df_cleaned[column] = self.remove_punctuations(self.df_cleaned, [column])[column]
                self.df_cleaned[column] = self.remove_digits(self.df_cleaned, [column])[column]
                self.df_cleaned[column] = self.remove_characters(self.df_cleaned, [column], char=self.char)[column]
                self.df_cleaned[column] = self.remove_stopwords(self.df_cleaned, [column], stopwords=list(self.stopwords))[column]
            else:
                self.df_cleaned[column] = self.df[column]

        return self.df_cleaned

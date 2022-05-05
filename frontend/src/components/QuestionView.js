import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      currentSearchTerm: ''
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `http://localhost:5000/questions?page=${this.state.page}&currentCategory=${this.state.currentCategory}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  getAnsByCategory(id) {
    $.ajax({
      url: `/categories/${id}/questions?page=${this.state.page}&currentCategory=${this.state.categories[id]}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  }

  resetCategory() {
    this.setState({ page: 1, currentCategory: null, searchTerm: '' }, () => {
      return this.getQuestions()
    });
  }

  selectPage(num) {
    this.setState({ page: num }, () => {
      if(this.state.currentSearchTerm) {
        return this.submitSearch(this.state.currentSearchTerm)
      }
      if(this.state.currentCategory) {
        const category_id = Object.entries(this.state.categories).find(([key, val]) => val === this.state.currentCategory)[0]
        return this.getByCategory(category_id)
      }
      return this.getQuestions()
    });
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 2);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    this.setState( (state) => {
      if(!this.state.currentCategory || this.state.currentCategory !== this.state.categories[id]) {
        return {page: 1, currentSearchTerm: ''}
      } else {
        return {currentSearchTerm: ''}
      }
    }, () => this.getAnsByCategory(id))
  };

  getBySearchTerm = (searchTerm) => {
    this.setState( (state) => {
      if(!this.state.currentSearchTerm || this.state.currentSearchTerm !== searchTerm) {
        return {page: 1, currentSearchTerm: searchTerm, currentCategory: null}
      } else {
        return {currentCategory: null}
      }
    }, () => this.submitSearch(searchTerm))
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search?page=${this.state.page}&currentCategory=${this.state.currentCategory}`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.resetCategory();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.resetCategory();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {this.state.categories[id]}
                <img
                  className='category'
                  alt={`${this.state.categories[id].toLowerCase()}`}
                  src={`${this.state.categories[id].toLowerCase()}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.getBySearchTerm} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;

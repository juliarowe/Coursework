class Modification
  include Mongoid::Document
  field :suggestion, type: String

  belongs_to :original, polymorphic: true
  has_many :votes, as: :rateable

  validates :suggestion, presence: true, length: { minimum: 2 }


  def rating
    if self.votes.count > 0
      vote_sum = self.votes.all.inject(0) { |sum, vote| sum + vote.value }
      vote_sum / votes.count
    else
      0
    end
  end
end

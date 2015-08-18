# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/
#

jQuery ->
  ingr_count = 3
  step_count = 3
  $("#add-ingredient").click (event)->
    to_add = '<div class="field ingredients-field">'
    to_add += '<div><label for="recipe_recipe_ingredients_attributes_' + ingr_count
    to_add += '_quantity">Quantity</label>'
    to_add += '<input type="text" name="recipe[recipe_ingredients_attributes]['
    to_add += ingr_count + '][quantity]" id="recipe_recipe_ingredients_attributes_'
    to_add += ingr_count + '_quantity"></div>'
    to_add += '<div><label for="recipe_recipe_ingredients_attributes_' + ingr_count + '_ingredient">Ingredient</label>'
    to_add += '<input type="text" name="recipe[recipe_ingredients_attributes]['
    to_add += ingr_count + '][ingredient]" id="recipe_recipe_ingredients_attributes_'
    to_add += ingr_count + '_ingredient</div>">'
    to_add += '</div>'
    $(".ingredients").append(to_add)
    ingr_count++

  $("#add-step").click (event)->
    to_add = '<div class="field steps-field">'
    to_add += '<div><label for="recipe_steps_attributes_' + step_count + '_'
    to_add += (step_count + 1) + '">'+ (step_count + 1) + '</label></div>'
    to_add += '<textarea name="recipe[steps_attributes]['
    to_add += step_count + '][instruction]" id="recipe_steps_attributes_'
    to_add += step_count + '_instruction"></textarea></div>'
    $(".steps").append(to_add)
    step_count++

  $(".mod-toggle").click (event) ->
    origId = $(event.target).attr('id')
    origId = origId.substr(8, origId.length)
    if $(event.target).hasClass("fa-comment")
      $(".suggestions").hide("fast")
      $(".fa-comment-o").removeClass("fa-comment-o").addClass("fa-comment")
      $(event.target).removeClass("fa-comment").addClass("fa-comment-o")
      $("#orig-mods-" + origId).show("fast")
      $(".new-mod-form").show("fast")
    else
      $(".new-mod-form").hide("fast")
      $(".suggestions").show("fast")
      $(".fa-comment-o").removeClass("fa-comment-o").addClass("fa-comment")

  $(".submit-mod").click (event) ->
    suggestion = $(event.target).parent().find(".new-mod").val()
    original_id = $(event.target).parent().find(".new-mod").attr('id')
    $.ajax
      type: "POST"
      data: { suggestion: suggestion, original_id: original_id }
      url: "/modifications/"
      success: (data) ->
        location.reload()
      error: (xhr, status, errorThrown) ->
        location.reload()

  $(".submit-sub").click (event) ->
    recipe_id = $(event.target).attr('id');
    recipe_id = recipe_id.substr(1, recipe_id.length - 1);
    subscriber = $("#add-subscriber").val();
    $.ajax
      type: "POST"
      data: { subscriber: subscriber, recipe_id: recipe_id }
      url: "/subscribers/"
      success: (data) ->
        alert "Congratulations! You're subscribed!"
      error: (data) ->
        alert "Error"


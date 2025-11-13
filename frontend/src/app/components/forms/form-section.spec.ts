import { FormSection } from '#components/forms';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('FormSection', () => {
  let component: FormSection;
  let fixture: ComponentFixture<FormSection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormSection],
    }).compileComponents();

    fixture = TestBed.createComponent(FormSection);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
